# Changes

## Version 2.0.0

### New

- `unitroots/` holds the data loading and the tests; the analyses and the unit tests use it.
- The three ADF models of version 1 are all reported, with lags chosen by AIC (as in version 1) and by BIC, next to
  KPSS (null of stationarity) and the ADF p-value for every number of lags from 0 to 14.
- The order of integration is tested from the highest difference down (Dickey and Pantula, 1987).
- Card spending is studied per week and in real terms, prices in logs; the `ito` price index is used as an
  independent check on the CPI.
- Zivot–Andrews test (Model A: constant, trend and one shift in level) for monthly inflation, the break test version 1
  named as its next step.
- Unit tests (`tests/run_tests.py`): the ADF regression and its AIC/BIC lag choice estimated directly by OLS, the KPSS
  statistic from its formula, the eight ADF statistics printed by version 1, a calendar computed with `datetime`,
  simulated series with a known answer and a direct search for the Zivot–Andrews statistic and break date.
- Three analyses, three figures, CSV tables, and a project note that writes out the equations of every model and
  test used in the code and whose numbers are written from the tables.
- `README.md` (replacing `README.txt`), `CITATION.cff`, `requirements.txt`, `.gitignore`, a GitHub Actions workflow
  that runs the tests.

### Corrections to version 1

| # | Version 1 | Version 2 |
|---|---|---|
| 1 | The notebook ran only with hidden state: `credit` and `tufe` are used before any cell defines them, and the execution counts skip 88, 94 and 101. Run from the top, it stops with a `NameError`. | Every result is produced by scripts that run from a clean start; the eight ADF statistics of version 1 are reproduced to 1e-8. |
| 2 | Three models were defined, but every test used Model 3, and the order of integration was found by testing upward from the level. Each ADF test assumes at most one unit root, so testing upward is not consistent with it. | All three models and two lag criteria are reported (Table 1 of the note); the order is tested from the top down. |
| 3 | `credit` and `tufe` were found I(2) from their levels. Both grow exponentially (CPI ×10.7, card spending ×38 over the sample), so the change in the level rises with the level even when the growth rate has no trend. | Prices and card spending are tested in logs. With a break in mean inflation in autumn 2021, log prices are I(1). |
| 4 | Card spending was tested as published. One more Friday in the month raises it by 0.229 in logs (log(5/4) = 0.223); the number of Fridays explains 0.87 of the variance of its monthly log change. | Spending is divided by the number of Fridays (weekly spending) and by the CPI (real spending). |
| 5 | A separate OLS regression of each series on a constant and a trend was used to judge the trend ("trend coefficient 12.9182, p-value 0.000"). For a series with a unit root the t-statistics of this regression are not valid, and its trend coefficient is not the one in the ADF regression. | Removed. The choice between Models 2 and 3 is stated in the note and both are reported. |
| 6 | Wording that contradicts the numbers: for `credit` the absolute ADF statistic (0.76) was said to be "above the critical values"; for its first difference, "the null hypothesis is rejected and the series still contains a unit root"; "the initial analysis before 1979"; the `usd` series was said to be "analyzed in SECTION 1" (it is Section 2). | The note states each result with its p-value and lag count. |
| 7 | The `ito` series was loaded but not used. | Used as a second price index (analyses 2 and 3). |
| 8 | Breaks were seen in the graphs ("distortions" in `credit` in 2022–2024, "irregularities" in `tufe` in 2018–2020 and 2022–2024) and break tests were listed, but none was run. | Zivot–Andrews test (analysis 3). |
| 9 | The README described ARIMA, VAR, impulse responses and Zivot–Andrews and Perron tests, none of which is in the notebook, and called the series "Stationary at I(2)". It was a `.txt` file, so GitHub did not render it, and its citation pointed to `USD_CREDIT_TUFE` instead of this repository. | The README describes only what the repository does; the citation points here. |
| 10 | `.ipynb_checkpoints/` was committed. | Ignored by `.gitignore`. Version 1 kept as `legacy/usd_credit_tufe_v1.ipynb` and `legacy/README_v1.txt`; the original files remain in the `v1.0.0` release. |

## Version 1.0.0

First version: a notebook applying the ADF test (Model 3, at most 14 lags chosen by AIC) to card spending, the USD
loan rate and the CPI, with line, ACF and PACF plots.
