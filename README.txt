This project presents a comprehensive analysis of various economic indicators sourced from the Central Bank of Turkey's (CBRT) EVDS data distribution system, focusing on Turkey's banking, consumer spending, and inflationary trends. Through rigorous stationarity and unit root testing, Vector Autoregression (VAR) modeling, and impact-response analysis, this study aims to uncover the underlying dynamics within Turkey's macroeconomic environment. Ultimately, the findings will contribute valuable insights toward effective policy recommendations for the Turkish banking sector.

## Data Overview

The datasets used in this analysis were sourced from CBRT's EVDS system and the Istanbul Chamber of Commerce (ITO):

1. **TOTAL (Thousand TRY)**  
   - **Description**: Monthly data on bank and credit card spending as reported by the CBRT.  
   - **Type**: Flow data  
   - **Unit**: Thousand TRY  

2. **Commercial Loans (Issued in USD)**  
   - **Description**: Weighted average interest rates on loans issued by banks in USD.  
   - **Type**: Flow data  
   - **Unit**: Percentage (%)  

3. **CPI Special Coverage Indicators (2003=100)**  
   - **Description**: Consumer Price Index (CPI) reported by TURKSTAT, serving as a benchmark for price-level changes.  
   - **Type**: Price index data  

4. **General Index (ITO 1995=100)**  
   - **Description**: Cost of Living Index for wage earners, published by the Istanbul Chamber of Commerce.  
   - **Type**: General index  
   - **Base Year**: 1995=100  

## Project Objectives

The following analyses were conducted on the monthly data series, aiming to evaluate long-term equilibrium trends, stationarity, and responsiveness to shocks within the Turkish economy:

- **Stationarity and Unit Root Testing**  
  Each series underwent a detailed visual and statistical examination to identify trends, seasonality, and potential non-stationarity. Augmented Dickey-Fuller (ADF) tests were applied to confirm stationarity and determine the order of differencing necessary for each series.
## Results and Key Insights

### Summary of Stationarity Testing

The ADF test results indicated varying levels of stationarity among the variables:

1. **Consumer Price Index (`tufe`)**  
   - The `tufe` series required differencing twice to achieve stationarity, indicating $tufe_t \sim I(2)$. This high integration order suggests the presence of a strong trend component, with the index likely responding persistently to economic shocks and demonstrating prolonged deviations from its mean.

2. **USD-denominated Commercial Loan Rates (`usd`)**  
   - Stationarity was achieved after the first difference, suggesting $usd_t \sim I(1)$. This result aligns with typical financial time series behavior, where interest rates often follow a random walk, stabilizing upon first differencing.

3. **Bank and Credit Card Spending (`credit`)**  
   - Similar to `tufe`, the `credit` series was found to be stationary only after the second difference, with $credit_t \sim I(2)$. This reflects persistent growth trends in consumer credit spending, likely driven by underlying economic factors such as income growth and credit accessibility.

### Modeling Implications and Considerations

The differing integration orders across the series have several implications for time series modeling:

- **ARIMA Modeling**: 
   - For `tufe` and `credit`, an ARIMA model with two levels of differencing (e.g., ARIMA(p,2,q)) may be appropriate to capture the trends observed. In contrast, the `usd` series is likely best suited for a simpler ARIMA model with one differencing step (e.g., ARIMA(p,1,q)).

- **Addressing Structural Breaks**:
   - Given the presence of potential structural breaks, especially in the `tufe` series, alternative unit root tests (e.g., Zivot-Andrews or Perron tests) could enhance robustness by accommodating shifts in the data. This would be particularly beneficial for series exposed to macroeconomic shocks, policy changes, or global volatility.

## Conclusion

In this portfolio project, we aimed to illustrate core time series methodologies by applying stationarity tests and examining integration orders across key economic indicators in Turkey. Through this analysis, we have demonstrated how different variables require tailored differencing techniques to achieve stationarity, a crucial step in effective time series modeling. The insights derived here not only underscore the importance of testing for stationarity but also highlight the need for flexible approaches that account for structural breaks and other complexities in economic data.

These findings lay a foundation for more advanced econometric modeling, providing a robust basis for forecasting and policy analysis within Turkey's dynamic economic landscape. Thank you for reading this project—I hope it provides valuable insights and lays the groundwork for further exploration in macroeconomic time series analysis.

## Contact Information

The author of this project, a recent graduate (July 2024) of the Department of Econometrics at Ankara Hacı Bayram Veli University, can be reached at:

- **Email**: myucanlar@gmail.com  
- **Alternate Email**: mikbal.yilmaz@gmx.com  

## Acknowledgments

Data sources:  
- **CBRT (Central Bank of Turkey)** - [EVDS Data Distribution System](https://evds2.tcmb.gov.tr/index.php?/evds/serieMarket) 
