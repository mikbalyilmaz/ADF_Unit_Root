"""Unit tests. Run from the repository root:  python tests/run_tests.py

Each result is compared with an independent computation: the ADF regression and its lag choice estimated
directly by OLS, the KPSS statistic from its formula, the numbers printed by version 1, a calendar computed with
datetime, simulated series with a known answer, and a direct search for the Zivot-Andrews statistic and break
date.
"""

import datetime as dt
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from unitroots import adf, adf_by_lag, fridays, integration_order, kpss_test, load, transformed, za_test  # noqa: E402

failed = 0


def check(name, ok):
    global failed
    print(f"{'ok' if ok else 'FAIL':<5}{name}")
    if not ok:
        failed += 1


df = load()
check("data: 127 consecutive months from 2014-03 to 2024-09, no missing values",
      len(df) == 127 and df.index[0] == pd.Timestamp("2014-03-01") and df.index[-1] == pd.Timestamp("2024-09-01")
      and not df.isna().any().any())

# Fridays: compare with a day-by-day count using datetime
ok = True
for t, k in fridays(df.index).items():
    day, n = dt.date(t.year, t.month, 1), 0
    while day.month == t.month:
        n += day.weekday() == 4
        day += dt.timedelta(days=1)
    ok &= n == k
check("number of Fridays per month equals a day-by-day count", ok)

# ADF statistic: the t-statistic of y_{t-1} in the regression of version 1, estimated directly
x = np.log(df["tufe"]).diff().dropna()
k = 3
dy = x.diff()
X = pd.DataFrame({"ylag": x.shift(1), "const": 1.0, "trend": np.arange(len(x), dtype=float)})
for j in range(1, k + 1):
    X[f"d{j}"] = dy.shift(j)
data = pd.concat([dy.rename("dy"), X], axis=1).dropna()
t_direct = sm.OLS(data["dy"], data.drop(columns="dy")).fit().tvalues["ylag"]
check("ADF statistic (Model 3, fixed lags) equals the OLS t-statistic computed directly",
      abs(adf(x, "ct", maxlag=k, autolag=None)["stat"] - t_direct) < 1e-10)

# Version 1, reproduced (values printed in its notebook)
printed = {("credit", 0): -0.761734273279262, ("credit", 1): 2.4217977752522803, ("credit", 2): -4.161841593471332,
           ("usd", 0): -2.34841386835875, ("usd", 1): -12.063151112469942,
           ("tufe", 0): 2.547393283265738, ("tufe", 1): -1.37679770041913, ("tufe", 2): -4.994473442233126}
ok = True
for (name, d), value in printed.items():
    s = df[name]
    for _ in range(d):
        s = s.diff()
    ok &= abs(adf(s, "ct", 14, "AIC")["stat"] - value) < 1e-8
check("ADF statistics of version 1 are reproduced to 1e-8 (8 tests)", ok)

# Known answers on simulated series
rng = np.random.default_rng(7)
walk = pd.Series(np.cumsum(rng.standard_normal(400)))
noise = pd.Series(rng.standard_normal(400))
check("ADF: rejects for white noise, not for a random walk",
      adf(noise, "c")["p"] < 0.01 and adf(walk, "c")["p"] > 0.10)
check("KPSS: does not reject for white noise, rejects for a random walk",
      kpss_test(noise, "c")["p"] > 0.05 and kpss_test(walk, "c")["p"] < 0.05)
i2 = pd.Series(np.cumsum(np.cumsum(rng.standard_normal(400))))
check("integration order from the top down: 0 for noise, 1 for a random walk, 2 for its cumulative sum",
      [integration_order(s, "c")[0] for s in (noise, walk, i2)] == [0, 1, 2])
check("adf_by_lag uses exactly k lags", all(adf(walk, "c", maxlag=k, autolag=None)["lags"] == k for k in (0, 5, 9))
      and len(adf_by_lag(walk, "c", range(0, 4))) == 4)

# ADF lag choice: AIC and BIC over k = 0..14 on the common sample of T* = N - 1 - 14 observations, then the
# chosen k re-estimated on all usable observations (the procedure described in the note)
x = np.log(df["tufe"]).diff().dropna()
y, pmax = x.values, 14
dy = np.diff(y)


def adf_ols(k, first):
    rows = range(first, len(dy))  # dy[t] = y[t+1] - y[t]
    X = np.array([[1.0, y[t]] + [dy[t - j] for j in range(1, k + 1)] for t in rows])
    return sm.OLS(np.array([dy[t] for t in rows]), X).fit()


ok = True
for ic in ("AIC", "BIC"):
    crit = [getattr(adf_ols(k, pmax), ic.lower()) for k in range(pmax + 1)]
    k_best = int(np.argmin(crit))
    r = adf(x, "c", pmax, ic)
    ok &= r["lags"] == k_best and abs(r["stat"] - adf_ols(k_best, k_best).tvalues[1]) < 1e-10
check("ADF lag choice by AIC and BIC on the common sample, then re-estimation, done directly", ok)

# KPSS: the statistic from its formula with the bandwidth reported by the test
e = x.values - x.values.mean()
T = len(e)
ell = kpss_test(x, "c")["lags"]
gam = [e[i:] @ e[:T - i] / T for i in range(ell + 1)]
lrv = gam[0] + 2 * sum((1 - i / (ell + 1)) * gam[i] for i in range(1, ell + 1))
eta = (np.cumsum(e) ** 2).sum() / T**2 / lrv
check("KPSS statistic equals its formula (partial sums, Bartlett long-run variance)",
      abs(kpss_test(x, "c")["stat"] - eta) < 1e-10)

# Zivot-Andrews (Model A): statistic and break date from a direct search over OLS regressions with a constant,
# a trend, the shift DU_t = 1 for t > T_B, the lagged level and the lags chosen by the ADF regression with trend
s = transformed(df)["log_tufe"].diff().dropna()
r = za_test(s, "c", 14, "AIC")
y, k = s.values, adf(s, "ct", 14, "AIC")["lags"]
n, dy, best = len(y), np.diff(y), None
for tb in range(int(0.15 * n), n - int(0.15 * n)):
    rows = range(k + 1, n)
    X = np.array([[1.0, float(t > tb), float(t), y[t - 1]] + [dy[t - 1 - j] for j in range(1, k + 1)] for t in rows])
    t_alpha = sm.OLS(np.array([dy[t - 1] for t in rows]), X).fit().tvalues[3]
    best = (t_alpha, tb) if best is None or t_alpha < best[0] else best
check(f"Zivot-Andrews statistic and break ({r['break']:%Y-%m}) equal a direct search",
      best[1] == r["break_index"] and abs(best[0] - r["stat"]) < 1e-8 and r["lags"] == k)

print(f"\n{failed} check(s) failed.")
sys.exit(1 if failed else 0)
