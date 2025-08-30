# Time Series Analysis of Türkiye’s Macroeconomic Indicators  

Most real-world time series are nonstationary, and this project explores different types of nonstationarity in key macroeconomic indicators for Türkiye.  

Using datasets from the **Central Bank of Türkiye (CBRT) EVDS system**, **TURKSTAT**, and the **Istanbul Chamber of Commerce (ITO)**, the project applies unit root and stationarity testing, **Vector Autoregression (VAR)** modeling, and **impulse-response analysis** to uncover underlying dynamics in Türkiye’s banking, consumer spending, and inflation trends. The results provide insights with potential relevance for monetary and banking policy.  

---

## Data Sources  

1. **TOTAL (Thousand TRY)**  
   - Monthly bank and credit card spending (CBRT)  
   - Flow data, Thousand TRY  

2. **Commercial Loans (Issued in USD)**  
   - Weighted average interest rates on USD-denominated bank loans  
   - Flow data, Percentage (%)  

3. **CPI Special Coverage Indicators (2003=100)**  
   - Consumer Price Index (CPI) reported by TURKSTAT  
   - Price index data  

---

## Objectives  

The analysis evaluates long-term equilibrium relationships, stationarity properties, and responsiveness to shocks in the Turkish economy:  

- **Stationarity and Unit Root Testing**  
  - Visual inspection and formal tests to detect trends, seasonality, and persistence  
  - Augmented Dickey-Fuller (ADF) tests to confirm stationarity and identify differencing order  

- **Econometric Modeling**  
  - ARIMA specifications based on stationarity results  
  - VAR modeling and impulse-response functions for dynamic interactions  
  - Consideration of structural breaks (e.g., Zivot-Andrews, Perron tests) to capture policy shifts or external shocks  

---

## Key Findings  

- **Consumer Price Index (`tufe`)** → Stationary at second difference (I(2)), showing high persistence and slow adjustment to shocks.  
- **USD-denominated Loan Rates (`usd`)** → Stationary at first difference (I(1)), consistent with typical financial series.  
- **Credit Card Spending (`credit`)** → Stationary at second difference (I(2)), reflecting a persistent upward trend in consumption.  

**Modeling Implications:**  
- CPI (`tufe`) and Credit (`credit`) → ARIMA(p, 2, q)  
- USD Loan Rates (`usd`) → ARIMA(p, 1, q)  
- Structural break tests are recommended for robustness.  

---

## Conclusion  

This project demonstrates fundamental time series econometric methods applied to Türkiye’s macroeconomic data.  

**Main insights:**  
- Different series require different stationarity treatments  
- Unit root testing is essential for reliable modeling  
- Accounting for structural breaks improves robustness  
- Results lay the groundwork for policy-oriented econometric modeling  

---

## Author  

**Muhammed İkbal Yılmaz**  
Graduate (July 2024), Department of Econometrics, Hacı Bayram Veli University  

- 📧 Email: [myucanlar@gmail.com](mailto:myucanlar@gmail.com)  
- 📧 Alternate: [mikbal.yilmaz@gmx.com](mailto:mikbal.yilmaz@gmx.com)  
- 🔗 LinkedIn: [linkedin.com/in/muhammed-ikbal-yilmaz-36622a276](https://www.linkedin.com/in/muhammed-ikbal-yilmaz-36622a276)  

---

## Acknowledgments  

- **Central Bank of Türkiye (CBRT) – EVDS:** [Link](https://evds2.tcmb.gov.tr/index.php?/evds/serieMarket)  
- **TURKSTAT – CPI Data**  
- **Istanbul Chamber of Commerce (ITO) – Sectoral Data**  

---

© 2024 Muhammed İkbal Yılmaz. All rights reserved.  
