"""Analysis 2: integration orders with the three ADF models, two lag criteria and a stationarity test.

Why: version 1 defined three ADF models but used only Model 3 (constant and trend) for every series and every
difference, chose lags by AIC only, and tested upward from levels. The order of integration of a series
should not depend on such choices without the reader knowing it. Here the tests are run on the transformed
series of version 2 (logs; card spending per week and deflated by the CPI), for all three models and for AIC
and BIC, from the second difference downward (Dickey and Pantula, 1987), and checked with the KPSS test,
whose null hypothesis is stationarity.

Model choice: levels of trending series (log prices, log card spending) use Model 3; the USD loan rate, which
has no reason to trend, uses Model 2; differences use Model 2, because a trend in a growth rate would mean a
quadratic trend in the level.
"""

from common import SERIES, label, save_table
from unitroots import adf, adf_by_lag, integration_order, kpss_test
from unitroots.style import RED, SERIES as LINE_STYLES, end_label, free_axis, may_touch, save_figure, use_style, \
    value_axis

ORDER = ["log_credit_weekly", "log_credit_real", "usd", "log_tufe", "log_ito"]
MODELS = {name: {0: ("c" if name == "usd" else "ct"), 1: "c", 2: "c"} for name in ORDER}


def diff(x, d):
    for _ in range(d):
        x = x.diff()
    return x


grid = []
for name in ORDER:
    for d in (0, 1, 2):
        x = diff(SERIES[name], d)
        row = {"series": name, "difference": d}
        for model in ("n", "c", "ct"):
            for ic in ("AIC", "BIC"):
                r = adf(x, model, 14, ic)
                row[f"{model}_{ic}_stat"], row[f"{model}_{ic}_p"], row[f"{model}_{ic}_lags"] = r["stat"], r["p"], r["lags"]
        k = kpss_test(x, "ct" if (d == 0 and MODELS[name][0] == "ct") else "c")
        row["kpss_stat"], row["kpss_p"], row["kpss_cv5"] = k["stat"], k["p"], k["cv5"]
        grid.append(row)
save_table(grid, "table4_adf_grid")

orders = []
for name in ORDER:
    entry = {"series": name}
    for ic in ("AIC", "BIC"):
        order, steps = integration_order(SERIES[name], MODELS[name], 0.05, 2, maxlag=14, autolag=ic)
        entry[f"order_{ic}"] = order
        entry[f"steps_{ic}"] = "; ".join(f"d={d}: p={r['p']:.3f} (k={r['lags']})" for d, r in steps)
    orders.append(entry)
save_table(orders, "table5_orders")
for o in orders:
    print(o)

# p-value against the number of lags for the first differences (Model 2)
FIRST = ["log_credit_real", "usd", "log_tufe", "log_ito"]
by_lag = {name: adf_by_lag(SERIES[name].diff(), "c", range(0, 15)) for name in FIRST}
chosen = {name: {ic: adf(SERIES[name].diff(), "c", 14, ic)["lags"] for ic in ("AIC", "BIC")} for name in FIRST}
save_table([{"series": n, "lags": k, "p": p} for n in FIRST for k, p in by_lag[n].items()], "table6_p_by_lag")

# Annual pattern in real card spending growth, which is why AIC keeps 12 lags for it
from statsmodels.tsa.stattools import acf  # noqa: E402
growth = SERIES["log_credit_real"].diff().dropna()
save_table([{"lag": k, "acf": float(v)} for k, v in enumerate(acf(growth, nlags=13)) if k in (1, 2, 3, 6, 12)],
           "table6b_credit_acf")

use_style()


def draw():
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(4.75, 2.6), constrained_layout=True)
    for name, (c, ls, mk) in zip(FIRST, LINE_STYLES):
        ks = list(by_lag[name])
        ps = [by_lag[name][k] for k in ks]
        ax.plot(ks, ps, color=c, ls=ls, lw=1.2, marker=mk, ms=2.6, clip_on=False)
        for ic, marker, size in (("AIC", "o", 7.5), ("BIC", "s", 5)):
            k = chosen[name][ic]
            ax.plot([k], [by_lag[name][k]], marker=marker, ms=size, mfc="none", mec=c, mew=1.0, ls="none",
                    clip_on=False)
        end_label(ax, ks[-1], ps[-1], "Δ " + label(name), c, dx=5)
    ref = ax.axhline(0.05, color=RED, lw=1.0, ls=(0, (1, 1.4)))
    may_touch(ref)
    ax.annotate("5%", xy=(0.5, 0.05), xytext=(0, 2), textcoords="offset points", xycoords="data",
                ha="center", va="bottom", color=RED, fontsize=7, fontweight="bold")
    ax.set_xlabel("Number of lagged differences k")
    ax.set_xticks(range(0, 15, 2))
    ax.set_xlim(0, 14)
    free_axis(ax, "x")
    value_axis(ax, "y", 0, 1, 0.2)
    ax.set_title("ADF p-value (Model 2); circle: lag chosen by AIC, square: by BIC")
    return fig


save_figure("fig2_lags", draw, lambda: "Figure 2. ADF p-value of the first differences against the number of lags")
