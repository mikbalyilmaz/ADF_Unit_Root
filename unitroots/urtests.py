"""Unit root and stationarity tests, as thin, documented wrappers around statsmodels.

ADF  (Dickey and Fuller, 1979; Said and Dickey, 1984): H0 unit root. The three deterministic models of
     version 1 are regression = "n" (Model 1, none), "c" (Model 2, constant), "ct" (Model 3, constant and
     trend). p-values and critical values are those of statsmodels (MacKinnon response surfaces).
KPSS (Kwiatkowski et al., 1992): H0 stationarity around a constant ("c") or a trend ("ct"). statsmodels
     interpolates p-values from a table, so they are truncated to the range [0.01, 0.10].
ZA   (Zivot and Andrews, 1992), Model A as implemented in statsmodels (regression = "c"): the ADF regression
     with a constant, a linear trend and a shift in the intercept, DU_t = 1 for t > T_B. H0 unit root; alternative
     trend-stationarity with one shift in level at a date chosen by the data (the most negative t-statistic over
     the central 70% of the sample). The number of lags is chosen once, by the ADF regression with constant and
     trend and no break, and then used for every candidate date.

Author: Muhammed Ikbal Yilmaz
"""

import warnings

import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, kpss, zivot_andrews

V1_SETTINGS = {"maxlag": 14, "autolag": "AIC"}  # the lag settings of version 1


def adf(series, regression="ct", maxlag=14, autolag="AIC"):
    """ADF test; autolag=None uses exactly `maxlag` lagged differences."""
    x = np.asarray(series.dropna() if hasattr(series, "dropna") else series, dtype=float)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)  # statsmodels >= 0.15 announces a new return type
        stat, p, lags, nobs, crit, *_ = adfuller(x, maxlag=maxlag, regression=regression, autolag=autolag)
    return {"stat": float(stat), "p": float(p), "lags": int(lags), "nobs": int(nobs),
            "cv1": float(crit["1%"]), "cv5": float(crit["5%"]), "cv10": float(crit["10%"])}


def adf_by_lag(series, regression="c", lags=range(0, 15)):
    """ADF p-value for each fixed number of lagged differences."""
    return {k: adf(series, regression, maxlag=k, autolag=None)["p"] for k in lags}


def kpss_test(series, regression="c"):
    x = np.asarray(series.dropna(), dtype=float)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # statsmodels warns when the p-value is outside its table
        stat, p, lags, crit = kpss(x, regression=regression, nlags="auto")
    return {"stat": float(stat), "p": float(p), "lags": int(lags), "cv5": float(crit["5%"])}


def za_test(series, regression="c", maxlag=14, autolag="AIC"):
    """Zivot-Andrews test (Model A). `break` is the last month before the shift; the new regime starts the month
    after."""
    s = series.dropna()
    stat, p, crit, lags, bp = zivot_andrews(np.asarray(s, dtype=float), maxlag=maxlag, regression=regression,
                                            autolag=autolag)
    return {"stat": float(stat), "p": float(p), "lags": int(lags), "cv1": float(crit["1%"]),
            "cv5": float(crit["5%"]), "break_index": int(bp), "break": s.index[bp]}


def za_regression(series, result):
    """The Zivot-Andrews regression at the selected break, estimated directly by OLS:
    dy_t = mu + theta DU_t + beta t + alpha y_{t-1} + sum_j c_j dy_{t-j} + e_t,  DU_t = 1 for t > T_B.
    Returns the estimates and t-statistics of mu, theta, beta and alpha (t of alpha is the ZA statistic)."""
    y = np.asarray(series.dropna(), dtype=float)
    k, tb = result["lags"], result["break_index"]
    dy = np.diff(y)
    rows = range(k + 1, len(y))
    X = np.array([[1.0, float(t > tb), float(t), y[t - 1]] + [dy[t - 1 - j] for j in range(1, k + 1)] for t in rows])
    fit = sm.OLS(np.array([dy[t - 1] for t in rows]), X).fit()
    names = ("mu", "theta", "beta", "alpha")
    out = {f"{n}": float(fit.params[i]) for i, n in enumerate(names)}
    out.update({f"t_{n}": float(fit.tvalues[i]) for i, n in enumerate(names)})
    out["nobs"] = int(fit.nobs)
    return out


def integration_order(series, regression="c", level=0.05, max_order=2, **adf_kwargs):
    """Order of integration by testing from the highest difference down (Dickey and Pantula, 1987).

    Starting with the max_order-th difference, a unit root is tested in each lower difference as long as the
    previous test rejected. The order is the number of differences in the last series that rejected.
    `regression` is one model for all differences, or a dict {difference: model}.
    Returns (order, list of (difference, ADF result)).
    """
    steps = []
    order = None
    for d in range(max_order, -1, -1):
        x = series
        for _ in range(d):
            x = x.diff()
        model = regression[d] if isinstance(regression, dict) else regression
        res = adf(x, regression=model, **adf_kwargs)
        steps.append((d, res))
        if res["p"] < level:
            order = d
        else:
            break
    return (max_order + 1 if order is None else order), steps
