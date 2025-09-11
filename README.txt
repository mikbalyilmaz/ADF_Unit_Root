# Time Series Analysis of Türkiye’s Macroeconomic Indicators
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A reproducible econometric analysis exploring **nonstationarity** in Türkiye’s key macroeconomic indicators.  
Using data from the **Central Bank of Türkiye (CBRT) EVDS**, **TURKSTAT**, and the **Istanbul Chamber of Commerce (ITO)**, the project applies **unit root tests, ARIMA/VAR modeling, and impulse–response analysis** to examine relationships between credit, loan rates, and inflation.  
The results provide insights with potential policy relevance for monetary stability and banking.

---

## Data Sources
1. **TOTAL (Thousand TRY)**  
   - Monthly bank & credit card spending (CBRT)  
   - Flow data, Thousand TRY  

2. **Commercial Loans (USD)**  
   - Weighted average interest rates on USD-denominated bank loans  
   - Flow data, Percentage (%)  

3. **CPI Special Coverage Indicators (2003=100)**  
   - Consumer Price Index (TURKSTAT)  
   - Price index data  

---

## Objectives
The analysis evaluates long-term equilibrium, stationarity properties, and responsiveness to shocks:

- **Stationarity & Unit Root Testing**  
  - Visual inspection & Augmented Dickey-Fuller (ADF)  
  - Differencing order identification  
- **Econometric Modeling**  
  - ARIMA specifications based on integration order  
  - VAR & impulse–response functions for dynamics  
  - Structural break tests (Zivot-Andrews, Perron) for policy shifts  

---

## Key Findings
- **CPI (`tufe`)** → Stationary at I(2); highly persistent.  
- **USD Loan Rates (`usd`)** → Stationary at I(1); typical of financial series.  
- **Credit Card Spending (`credit`)** → Stationary at I(2); persistent consumption trend.  

**Modeling Implications:**  
- CPI (`tufe`) & Credit (`credit`) → ARIMA(p,2,q)  
- USD Loan Rates (`usd`) → ARIMA(p,1,q)  
- Structural breaks must be considered for robustness.  

---

## Quick Start

### Prerequisites
- Python ≥ 3.9  
- Packages: `numpy`, `pandas`, `matplotlib`, `statsmodels`

Install:
```bash
pip install numpy pandas matplotlib statsmodels
# or:
# pip install -r requirements.txt

Run in Jupyter Notebook
%run USD_CREDIT_TUFE.ipynb

Methodological Notes

Model: $X_t$ represents macro series (credit, usd, tufe).

ADF & Differencing: Ensures valid ARIMA/VAR estimation.

VAR–IRFs: Show shock transmission between inflation, credit, and loan rates.

Break Tests: Capture structural changes due to policy or external shocks.

Author

Muhammed İkbal Yılmaz
Graduate (July 2024), Department of Econometrics, Hacı Bayram Veli University

📧 Email: myucanlar@gmail.com

📧 Alternate: mikbal.yilmaz@gmx.com

🔗 LinkedIn: linkedin.com/in/muhammed-ikbal-yilmaz-36622a276

Acknowledgments

CBRT EVDS: Link

TURKSTAT – CPI Data

ITO – Sectoral Data

License

© Licensed under the MIT License — free to use, modify, and distribute with attribution.

How to Cite

Yılmaz, M. İ. (2025). Time Series Analysis of Türkiye’s Macroeconomic Indicators. GitHub. https://github.com/mikbalyilmaz/USD_CREDIT_TUFE

APA citation:
Yılmaz, M. İ. (2025). Time Series Analysis of Türkiye’s Macroeconomic Indicators. GitHub. Retrieved September 11, 2025, from https://github.com/mikbalyilmaz/USD_CREDIT_TUFE

BibTeX:

@misc{usd_credit_tufe_2025,
  author       = {Muhammed İkbal Yılmaz},
  title        = {Time Series Analysis of Türkiye’s Macroeconomic Indicators},
  year         = {2025},
  howpublished = {\url{https://github.com/mikbalyilmaz/USD_CREDIT_TUFE}},
  note         = {Accessed: 2025-09-11}
}

