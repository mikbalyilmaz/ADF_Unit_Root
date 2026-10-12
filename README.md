# ADF Unit Roots in Four Turkish Monthly Series

[![tests](https://github.com/mikbalyilmaz/ADF_Unit_Root/actions/workflows/tests.yml/badge.svg)](https://github.com/mikbalyilmaz/ADF_Unit_Root/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Version 2 of a small study of the order of integration of monthly Turkish series, March 2014 to September 2024
(127 months): bank and credit card spending, the interest rate on USD commercial loans, the consumer price index
and, new in version 2, the ITO price index as an independent check on the CPI. The augmented Dickey–Fuller (ADF)
test of version 1 is kept with its three models and its lag settings (at most 14 lagged differences, chosen by AIC).
Version 2 asks what the series contain before they are tested, whether the result depends on the model and the
number of lags, and whether inflation is better described as a unit root process or as a stationary series with a
break. A short project note explains why each analysis was done and what it shows, and writes out the mathematics
behind every model and test in the code.

## Contents

| Path | What it is |
|---|---|
| `unitroots/data.py` | Loads the data and checks it; Fridays per month; log, weekly and real transformations |
| `unitroots/urtests.py` | ADF, KPSS and Zivot–Andrews as thin wrappers around statsmodels; ADF over a range of lags; order of integration tested from the top down; the Zivot–Andrews regression at the break |
| `unitroots/style.py` | Shared figure style (Latin Modern Roman, fixed colours) |
| `tests/run_tests.py` | Unit tests: the ADF regression and its AIC/BIC lag choice estimated directly by OLS, the KPSS statistic from its formula, the output of version 1, a calendar computed with `datetime`, simulated series with a known answer, and a direct search for the Zivot–Andrews statistic and break date |
| `analysis/01_data.py` | Version 1 reproduced; calendar effect in card spending; exponential growth of prices (Figure 1) |
| `analysis/02_integration_order.py` | ADF under three models and two lag criteria, KPSS, p-value against the number of lags, order of integration (Table 1, Figure 2) |
| `analysis/03_breaks.py` | Zivot–Andrews test (Model A: constant, trend and a shift in level) for monthly inflation (Figure 3) |
| `analysis/run_all.py` | Runs the three analyses in order (about ten seconds) |
| `data/usd_credit_tufe_ito.xlsx` | The data of version 1, unchanged |
| `figures/` | Figures as PNG (300 dpi) and PDF, every reported table as CSV |
| `paper/adf_note.pdf` | Project note: data, equations of every model and test, the three analyses; `make_paper.py` writes all its numbers from `figures/*.csv` |
| `legacy/` | Version 1 (notebook and README), unchanged |
| `fonts/` | Latin Modern Roman (GUST Font License) |

## How to run

```
pip install -r requirements.txt
python tests/run_tests.py
cd analysis
python run_all.py
cd ../paper
python make_paper.py
xelatex adf_note.tex && xelatex adf_note.tex       # needs XeLaTeX
```

Seeds are fixed (only the horizontal jitter of Figure 1a and the simulated series of the tests are random), so every
number is the same at every run.

## Usage

```python
from unitroots import load, transformed, adf, kpss_test, za_test, za_regression, integration_order

df = load()                                   # credit, usd, tufe, ito; monthly index
s = transformed(df)                           # log_credit_weekly, log_credit_real, usd, log_tufe, log_ito
adf(s["usd"].diff(), "c", maxlag=14, autolag="AIC")       # stat, p, lags, nobs, critical values
kpss_test(s["log_tufe"].diff(), "c")                       # stat, p (within [0.01, 0.10]), lags, 5% value
r = za_test(s["log_tufe"].diff(), "c")                     # stat, p, lags, break (last month before the shift)
za_regression(s["log_tufe"].diff(), r)                     # estimates and t-statistics at that break
integration_order(s["log_ito"], {0: "ct", 1: "c", 2: "c"}, autolag="BIC")   # (order, steps)
```

## Main results

- **USD loan rate: I(1).** The first difference rejects a unit root under every model, both lag criteria and every
  number of lags up to six; KPSS does not reject its stationarity. Same conclusion as version 1.
- **Prices: I(1) with a break, not I(2).** In logs, monthly inflation does not reject a unit root with AIC
  (CPI: p = 0.137 with 6 lags; ITO: p = 0.112), and KPSS rejects stationarity. The Zivot–Andrews test rejects the unit
  root in favour of stationarity with a single shift in level (CPI: statistic −6.16 against −5.28 at 1%; ITO: −5.69);
  at the break the shift is significant (t = 4.53 for the CPI) and the trend is not (t = 1.16). The two
  indices place the break one month apart: after 2021-10 (CPI) and 2021-09 (ITO); mean monthly CPI inflation rises
  from 0.99% to 4.18%. The I(2) of version 1 is explained by testing the level of an exponentially growing series
  and ignoring the shift.
- **Card spending has a calendar effect.** The monthly figure behaves like the sum of weekly figures over the weeks
  ending on a Friday: the number of Fridays explains 0.87 of the variance of its monthly log change, and one more
  Friday raises spending by 0.229 in logs (log(5/4) = 0.223). After dividing by the number of Fridays and by the CPI,
  BIC and KPSS point to I(1); AIC picks 12 lags (annual pattern) and the test then loses power.

All numbers are in `figures/*.csv` and in the project note.

## Data

`data/usd_credit_tufe_ito.xlsx`, sheet `EVDS`, as used by version 1 (downloaded from the CBRT EVDS system):

| Column | Series (as described in version 1) | Unit |
|---|---|---|
| `credit` | Bank and credit card spending | thousand TL, monthly flow |
| `usd` | Weighted average interest rate on USD commercial loans | percent |
| `tufe` | Consumer price index | 2003 = 100 |
| `ito` | Istanbul Chamber of Commerce price index | index |

Version 1 did not record the EVDS series codes, so they are not given here.

## Changes from version 1

See [NEWS.md](NEWS.md): what was added and a table of the corrections to version 1.

## Citation

See [CITATION.cff](CITATION.cff), or:

> Yılmaz, M. İ. (2026). *ADF unit roots in four Turkish monthly series* (Version 2.0.0) [Computer software].
> https://github.com/mikbalyilmaz/ADF_Unit_Root

## License

MIT, see [LICENSE](LICENSE).
