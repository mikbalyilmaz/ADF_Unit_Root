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
from unitroots.style import AQUA, BLUE, MUTED, ORANGE, PURPLE, decimal_axis, save_figure, use_style

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
    fig, ax = plt.subplots(figsize=(7.0, 3.1), constrained_layout=True)
    for name, c, mk in zip(FIRST, (BLUE, AQUA, ORANGE, PURPLE), ("o", "s", "D", "^")):
        ks = list(by_lag[name])
        ax.plot(ks, [by_lag[name][k] for k in ks], color=c, lw=1.2, marker=mk, ms=3,
                label="Δ " + label(name))
        for ic, marker, size in (("AIC", "o", 9), ("BIC", "s", 6)):
            k = chosen[name][ic]
            ax.plot([k], [by_lag[name][k]], marker=marker, ms=size, mfc="none", mec=c, mew=1.1, ls="none")
    ax.axhline(0.05, color=MUTED, lw=0.8, ls=":")
    ax.text(1.005, 0.05, "5%", color=MUTED, fontsize=8, va="center", ha="left",
            transform=ax.get_yaxis_transform())
    ax.set_xlabel("Number of lagged differences k")
    ax.set_ylabel("ADF p-value (Model 2)")
    ax.set_xticks(range(0, 15))
    ax.set_ylim(-0.02, 1.0)
    decimal_axis(ax)
    ax.set_title("Lags chosen by AIC (circle) and BIC (square)")
    ax.legend(loc="upper left", fontsize=7.5)
    return fig


save_figure("fig2_lags", draw, lambda: "Figure 2. ADF p-value of the first differences against the number of lags")
