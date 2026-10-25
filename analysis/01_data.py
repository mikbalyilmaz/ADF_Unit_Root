"""Analysis 1: reproduce version 1, then look at what the series contain before testing them.

Why: version 1 tested the series in levels, with Model 3 (constant and trend), at most 14 lags chosen by AIC,
and found credit and CPI to be I(2). Before any test is interpreted, two properties of the data matter:
(a) the monthly credit values move with the number of Fridays in the month, which points to sums of weekly
    figures, so part of their month-to-month variation is a calendar effect;
(b) the price index and credit grow roughly exponentially, so their monthly changes in levels grow with the
    level itself, while their changes in logs (growth rates) do not.

Design: the ADF tests of version 1 are repeated exactly; monthly log changes of credit are regressed on the
change in the number of each weekday in the month; the CPI is shown as monthly changes in index points and as
monthly log changes (inflation).
"""

import math

import numpy as np
import statsmodels.api as sm

from common import DATA, save_table
from unitroots import adf, weekday_count
from unitroots.style import BLUE, INK, fit_axis, free_axis, save_figure, use_style

# Version 1, reproduced: the eight tests it ran (raw series, Model 3, maxlag 14, AIC)
V1_TESTS = {"credit": 2, "usd": 1, "tufe": 2}  # highest difference tested by version 1
rows = []
for name, top in V1_TESTS.items():
    x = DATA[name]
    for d, series in list(((0, x), (1, x.diff()), (2, x.diff().diff())))[:top + 1]:
        r = adf(series, "ct", 14, "AIC")
        rows.append({"series": name, "difference": d, "stat": r["stat"], "p": r["p"], "lags": r["lags"],
                     "cv5": r["cv5"]})
save_table(rows, "table1_v1_reproduced")

# Calendar effect in credit
y = np.log(DATA["credit"]).diff()
cal = []
for wd, day in enumerate(("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")):
    k = weekday_count(DATA.index, wd).diff()
    fit = sm.OLS(y.iloc[1:], sm.add_constant(k.iloc[1:])).fit()
    cal.append({"weekday": day, "coef": float(fit.params.iloc[1]), "se": float(fit.bse.iloc[1]),
                "t": float(fit.tvalues.iloc[1]), "r2": float(fit.rsquared)})
save_table(cal, "table2_calendar")
fri = next(c for c in cal if c["weekday"] == "Friday")
counts = weekday_count(DATA.index, 4)

facts = [{
    "first_month": DATA.index[0].strftime("%Y-%m"), "last_month": DATA.index[-1].strftime("%Y-%m"),
    "months": len(DATA), "tufe_ratio": float(DATA.tufe.iloc[-1] / DATA.tufe.iloc[0]),
    "credit_ratio": float(DATA.credit.iloc[-1] / DATA.credit.iloc[0]),
    "ito_ratio": float(DATA.ito.iloc[-1] / DATA.ito.iloc[0]),
    "months_with_5_fridays": int((counts == 5).sum()), "log_5_over_4": math.log(5 / 4),
    "friday_coef": fri["coef"], "friday_se": fri["se"], "friday_r2": fri["r2"],
    "next_best_r2": max(c["r2"] for c in cal if c["weekday"] != "Friday"),
    "dtufe_first_year_mean": float(DATA.tufe.diff().iloc[1:13].mean()),
    "dtufe_last_year_mean": float(DATA.tufe.diff().iloc[-12:].mean()),
    "infl_first_year_mean": float(100 * np.log(DATA.tufe).diff().iloc[1:13].mean()),
    "infl_last_year_mean": float(100 * np.log(DATA.tufe).diff().iloc[-12:].mean()),
}]
save_table(facts, "table3_data_facts")
print(facts[0])

use_style()


def draw():
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(4.75, 2.05), constrained_layout=True,
                             gridspec_kw={"width_ratios": [1.25, 1, 1]})
    ax = axes[0]
    k = counts.diff().iloc[1:]
    rng = np.random.default_rng(0)                       # horizontal jitter only, so that points do not hide
    pct = 100 * y.iloc[1:]
    ax.scatter(k + rng.uniform(-0.12, 0.12, len(k)), pct, s=5, color=BLUE, lw=0, clip_on=False)
    xs = np.array([-1.3, 1.3])
    fit = sm.OLS(y.iloc[1:], sm.add_constant(k)).fit()
    ax.plot(xs, 100 * (fit.params.iloc[0] + fit.params.iloc[1] * xs), color=INK, lw=1.4)
    ax.set_xticks([-1, 0, 1], ["\u22121", "0", "+1"])
    ax.set_xlim(-1.5, 1.5)
    free_axis(ax, "x")
    fit_axis(ax, "y", pct, 20)
    ax.set_xlabel("Change in number of Fridays")
    ax.set_title("(a) Card spending, Δlog, %")
    ax = axes[1]
    d = DATA.tufe.diff()
    ax.plot(DATA.index, d, color=BLUE, lw=1)
    fit_axis(ax, "y", d, 50)
    ax.set_title("(b) ΔCPI, points")
    ax = axes[2]
    infl = 100 * np.log(DATA.tufe).diff()
    ax.plot(DATA.index, infl, color=BLUE, lw=1)
    ax.axhline(0, color=INK, lw=0.6)
    fit_axis(ax, "y", infl, 4)
    ax.set_title("(c) Inflation, %")
    for a in axes[1:]:
        a.xaxis.set_major_locator(mdates.YearLocator(4))
        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        free_axis(a, "x")
    return fig


save_figure("fig1_data", draw, lambda: "Figure 1. What the series contain before any test")
