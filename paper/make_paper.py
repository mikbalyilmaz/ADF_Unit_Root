"""Writes every number and table of the project note from ../figures/*.csv, so that the text cannot drift away
from the analysis. Run from inside paper/:  python make_paper.py

Output: numbers.tex (one macro per quoted number) and tab_grid.tex (table body ending with its bottom rule).
"""

import csv
from pathlib import Path

FIG = Path(__file__).resolve().parents[1] / "figures"
OUT = Path(__file__).resolve().parent


def read(name):
    with open(FIG / f"{name}.csv", newline="") as f:
        return list(csv.DictReader(f))


v1 = {(r["series"], int(r["difference"])): r for r in read("table1_v1_reproduced")}
cal = {r["weekday"]: r for r in read("table2_calendar")}
facts = read("table3_data_facts")[0]
grid = {(r["series"], int(r["difference"])): r for r in read("table4_adf_grid")}
orders = {r["series"]: r for r in read("table5_orders")}
acf12 = next(float(r["acf"]) for r in read("table6b_credit_acf") if r["lag"] == "12")
za = {(r["series"], int(r["difference"])): r for r in read("table7_zivot_andrews")}

NAMES = {"log_credit_real": "log real card spending per week", "usd": "USD loan rate", "log_tufe": "log CPI",
         "log_ito": "log ITO index", "log_credit_weekly": "log card spending per week"}


def build():
    def dec(x, d):
        return f"{float(x):.{d}f}"

    def pval(x):
        x = float(x)
        return "$<$0.001" if x < 0.001 else dec(x, 3)

    m = {}
    for (s, d), r in v1.items():
        key = {"credit": "Credit", "usd": "Usd", "tufe": "Tufe"}[s] + ["L", "D", "DD"][d]
        m[f"Vone{key}"] = dec(r["stat"], 2)
        m[f"Vone{key}p"] = pval(r["p"])
    m["Months"] = facts["months"]
    m["TufeRatio"] = dec(facts["tufe_ratio"], 1)
    m["CreditRatio"] = dec(facts["credit_ratio"], 0)
    m["ItoRatio"] = dec(facts["ito_ratio"], 1)
    m["FiveFridays"] = facts["months_with_5_fridays"]
    m["FriCoef"] = dec(facts["friday_coef"], 3)
    m["FriSe"] = dec(facts["friday_se"], 3)
    m["LogFiveFour"] = dec(facts["log_5_over_4"], 3)
    m["FriRsq"] = dec(facts["friday_r2"], 2)
    m["NextRsq"] = dec(facts["next_best_r2"], 2)
    m["DtufeFirst"] = dec(facts["dtufe_first_year_mean"], 1)
    m["DtufeLast"] = dec(facts["dtufe_last_year_mean"], 1)
    m["InflFirst"] = dec(facts["infl_first_year_mean"], 2)
    m["InflLast"] = dec(facts["infl_last_year_mean"], 2)

    def g(series, d, col):
        return grid[(series, d)][col]

    m["TufeDcAICp"] = pval(g("log_tufe", 1, "c_AIC_p"))
    m["TufeDcAICk"] = g("log_tufe", 1, "c_AIC_lags")
    m["TufeDcBICp"] = pval(g("log_tufe", 1, "c_BIC_p"))
    m["TufeDcBICk"] = g("log_tufe", 1, "c_BIC_lags")
    m["TufeDctAICp"] = pval(g("log_tufe", 1, "ct_AIC_p"))
    m["TufeDkpss"] = dec(g("log_tufe", 1, "kpss_stat"), 2)
    m["ItoDcAICp"] = pval(g("log_ito", 1, "c_AIC_p"))
    m["ItoDcAICk"] = g("log_ito", 1, "c_AIC_lags")
    m["ItoDkpss"] = dec(g("log_ito", 1, "kpss_stat"), 2)
    m["KpssCv"] = dec(g("log_tufe", 1, "kpss_cv5"), 3)
    m["RealDcAICp"] = pval(g("log_credit_real", 1, "c_AIC_p"))
    m["RealDcAICk"] = g("log_credit_real", 1, "c_AIC_lags")
    m["RealDcBICp"] = pval(g("log_credit_real", 1, "c_BIC_p"))
    m["RealDcBICk"] = g("log_credit_real", 1, "c_BIC_lags")
    m["RealDkpssp"] = dec(g("log_credit_real", 1, "kpss_p"), 3)
    m["RealAcfTwelve"] = dec(acf12, 2)
    m["NomDcAICp"] = pval(g("log_credit_weekly", 1, "c_AIC_p"))
    m["UsdLcp"] = pval(g("usd", 0, "c_AIC_p"))
    m["UsdLctp"] = pval(g("usd", 0, "ct_AIC_p"))
    m["UsdDcp"] = pval(g("usd", 1, "c_AIC_p"))

    def z(series, d, col, digits=2):
        return dec(za[(series, d)][col], digits)

    m["ZaTufe"] = z("log_tufe", 1, "stat")
    m["ZaTufeBreak"] = za[("log_tufe", 1)]["break"]
    m["ZaTufeBefore"] = z("log_tufe", 1, "mean_before")
    m["ZaTufeAfter"] = z("log_tufe", 1, "mean_after")
    m["ZaIto"] = z("log_ito", 1, "stat")
    m["ZaItoBreak"] = za[("log_ito", 1)]["break"]
    m["ZaItoBefore"] = z("log_ito", 1, "mean_before")
    m["ZaItoAfter"] = z("log_ito", 1, "mean_after")
    m["ZaCvOne"] = z("log_tufe", 1, "cv1")
    m["ZaCvFive"] = z("log_tufe", 1, "cv5")
    m["ZaUsdL"] = z("usd", 0, "stat")
    m["ZaUsdD"] = z("usd", 1, "stat")
    m["ZaReal"] = z("log_credit_real", 1, "stat")
    m["ZaRealLags"] = za[("log_credit_real", 1)]["lags"]
    m["ZaTufeLags"] = za[("log_tufe", 1)]["lags"]
    for key, s in (("Tufe", "log_tufe"), ("Ito", "log_ito")):
        m[f"Za{key}Theta"] = z(s, 1, "theta_pp")
        m[f"Za{key}Ttheta"] = z(s, 1, "t_theta")
        m[f"Za{key}Tbeta"] = z(s, 1, "t_beta")
    for s, key in (("log_credit_real", "Real"), ("usd", "Usd"), ("log_tufe", "Tufe"), ("log_ito", "Ito"),
                   ("log_credit_weekly", "Nom")):
        m[f"Order{key}AIC"] = orders[s]["order_AIC"]
        m[f"Order{key}BIC"] = orders[s]["order_BIC"]

    (OUT / "numbers.tex").write_text(
        "".join(f"\\newcommand{{\\{k}}}{{{v}}}\n" for k, v in m.items()), encoding="utf-8")

    lines = []
    for s in ("log_credit_real", "usd", "log_tufe", "log_ito"):
        for d in (0, 1):
            r = grid[(s, d)]
            name = NAMES[s] if d == 0 else "$\\Delta$ " + NAMES[s]
            cells = [name]
            for model in ("n", "c", "ct"):
                cells.append(f"{pval(r[f'{model}_AIC_p'])} ({r[f'{model}_AIC_lags']})")
            cells.append(f"{pval(r['c_BIC_p'])} ({r['c_BIC_lags']})")
            kp = float(r["kpss_p"])
            kp_text = "$\\le$0.01" if kp <= 0.01 else ("$\\ge$0.10" if kp >= 0.1 else dec(kp, 3))
            cells.append(kp_text)
            lines.append(" & ".join(cells) + " \\\\")
    lines.append("\\bottomrule")
    (OUT / "tab_grid.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")


build()
print("Wrote numbers.tex and tab_grid.tex.")
