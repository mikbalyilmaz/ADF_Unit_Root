# Time Series Analysis of Türkiye’s Macroeconomic Indicators  

Most time series in the real world are nonstationary, and there are various types of nonstationarity.  

This project provides a comprehensive analysis of selected economic indicators obtained from the Central Bank of Türkiye's (CBRT) EVDS data distribution system, with an emphasis on banking, consumer spending, and inflationary dynamics in Türkiye.  

The study applies stationarity and unit root testing, Vector Autoregression (VAR) modeling, and impact-response analysis to uncover the underlying dynamics of Türkiye’s macroeconomic environment. The results are expected to contribute to policy considerations in the Turkish banking sector.  

---

## Data Overview  

The datasets used in this analysis were obtained from the CBRT’s EVDS system and the Istanbul Chamber of Commerce (ITO):  

1. **TOTAL (Thousand TRY)**  
   - Monthly data on bank and credit card spending reported by the CBRT  
   - Flow data, Thousand TRY  

2. **Commercial Loans (Issued in USD)**  
   - Weighted average interest rates on loans issued by banks in USD  
   - Flow data, Percentage (%)  

3. **CPI Special Coverage Indicators (2003=100)**  
   - Consumer Price Index (CPI) reported by TURKSTAT, reflecting price-level changes  
   - Price index data  

---

## Project Objectives  

The analyses conducted on the monthly data series aimed to evaluate long-term equilibrium relations, stationarity properties, and responsiveness to shocks in the Turkish economy:  

- **Stationarity and Unit Root Testing**  
  Each series was examined visually and statistically to assess trends, seasonality, and nonstationarity.  
  Augmented Dickey-Fuller (ADF) tests were applied to confirm stationarity and determine the necessary order of differencing.  

---

## Results and Key Insights  

### Summary of Stationarity Testing  

- **Consumer Price Index (`tufe`)**  
  Required second differencing to achieve stationarity → tufe_t ~ I(2).  
  Indicates strong persistence and slow adjustment to shocks.  

- **USD-denominated Commercial Loan Rates (`usd`)**  
  Achieved stationarity after first differencing → usd_t ~ I(1).  
  Consistent with the behavior of financial time series.  

- **Bank and Credit Card Spending (`credit`)**  
  Required second differencing → credit_t ~ I(2).  
  Reflects persistent upward trends in consumer credit use.  

---

### Modeling Implications  

- **ARIMA Models**  
  - tufe and credit: ARIMA(p, 2, q)  
  - usd: ARIMA(p, 1, q)  

- **Structural Breaks**  
  Alternative unit root tests (e.g., Zivot-Andrews, Perron) may be necessary to account for structural changes due to policy shifts or external shocks.  

---

## Conclusion  

This project illustrates fundamental time series methodologies through an application to Türkiye’s key economic indicators.  

Main findings:  
- Stationarity requirements differ across variables, necessitating tailored approaches  
- Testing for stationarity is essential for reliable modeling  
- Consideration of structural breaks strengthens model robustness  

The results provide a foundation for further econometric modeling and contribute to a better understanding of the dynamics of the Turkish economy.  

---

## Author and Contact  

Muhammed İkbal Yılmaz  
Graduate (July 2024), Department of Econometrics, Hacı Bayram Veli University  

- Email: myucanlar@gmail.com  
- Alternate Email: mikbal.yilmaz@gmx.com  
- LinkedIn: www.linkedin.com/in/muhammed-ikbal-yilmaz-36622a276  

---

## Acknowledgments  

- Central Bank of Türkiye (CBRT) – EVDS Data Distribution System: https://evds2.tcmb.gov.tr/index.php?/evds/serieMarket  
- TURKSTAT – Consumer Price Index data  
- Istanbul Chamber of Commerce (ITO) – Sectoral data  

---

© All rights reserved sezinpersonal, 2024
