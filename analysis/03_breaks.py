"""Analysis 3: does a structural break explain the non-stationarity of inflation?

Why: version 1 saw "distortions" in 2018-2020 and 2022-2024 and named break tests (Zivot-Andrews among them) as
the next step, but did not run them. In analysis 2 the ADF test (Model 2) does not reject a unit root in
monthly inflation and the KPSS test rejects stationarity; both outcomes are also what a one-time shift in
the mean of a stationary series produces. The Zivot-Andrews test puts the break date where the evidence
against a unit root is strongest and asks whether the series is stationary around that shift.

Design: Zivot-Andrews Model A (regression "c": constant, linear trend and a shift in the intercept), at most 14
lags chosen by AIC, 15% trimming, for monthly inflation measured by the CPI and by the ITO index, the change in the USD loan rate and
its level, and the growth of real card spending per week. Mean monthly inflation is reported before and after
the estimated break, with the estimates of the ZA regression at the break (shift in percentage points and the
t-statistics of the shift, the trend and the lagged level).
"""

import numpy as np

from common import SERIES, label, save_table
from unitroots import za_regression, za_test
from unitroots.style import BLUE, MUTED, ORANGE, decimal_axis, save_figure, use_style

CASES = [("log_tufe", 1), ("log_ito", 1), ("usd", 0), ("usd", 1), ("log_credit_real", 1)]

rows = []
for name, d in CASES:
    x = SERIES[name].diff() if d else SERIES[name]
    r = za_test(x, "c", 14, "AIC")
    row = {"series": name, "difference": d, "stat": r["stat"], "p": r["p"], "lags": r["lags"], "cv1": r["cv1"],
           "cv5": r["cv5"], "break": r["break"].strftime("%Y-%m")}
    if name in ("log_tufe", "log_ito"):
        s = 100 * x.dropna()
        row["mean_before"] = float(s[s.index <= r["break"]].mean())
        row["mean_after"] = float(s[s.index > r["break"]].mean())
        row["months_after"] = int((s.index > r["break"]).sum())
        reg = za_regression(s, r)  # in percentage points; break and lags as chosen by the test
        assert abs(reg["t_alpha"] - r["stat"]) < 1e-8
        row.update({"theta_pp": reg["theta"], "t_theta": reg["t_theta"], "t_beta": reg["t_beta"],
                    "za_nobs": reg["nobs"]})
    rows.append(row)
    print(row)
keys = list(dict.fromkeys(k for r in rows for k in r))
save_table([{k: r.get(k, "") for k in keys} for r in rows], "table7_zivot_andrews")

use_style()


def draw():
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.8), constrained_layout=True, sharey=True)
    for ax, name, title in zip(axes, ("log_tufe", "log_ito"),
                               ("(a) CPI", "(b) ITO index")):
        s = 100 * SERIES[name].diff().dropna()
        row = next(r for r in rows if r["series"] == name)
        brk = np.datetime64(row["break"] + "-01")
        ax.plot(s.index, s, color=BLUE, lw=1)
        ax.axvline(brk, color=MUTED, lw=0.8, ls="--")
        ax.hlines(row["mean_before"], s.index[0], brk, color=ORANGE, lw=1.6, zorder=3)
        ax.hlines(row["mean_after"], brk, s.index[-1], color=ORANGE, lw=1.6, zorder=3)
        ax.set_title(title)
        ax.xaxis.set_major_locator(mdates.YearLocator(3))
        decimal_axis(ax)
    axes[0].set_ylabel("Monthly inflation (%)")
    return fig


save_figure("fig3_breaks", draw,
            lambda: "Figure 3. Monthly inflation, the Zivot-Andrews break and the mean in each regime")
