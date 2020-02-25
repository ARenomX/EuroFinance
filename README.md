# EuroFinance

The main strategies are stored in the Trader MkII file. The most updated next-day prediction strategy is day_predict_MkIII(coeff).

Coeff is the threshold percentage (use values between 1-10, 5 is good). for example, day_predict_MKII(5) will only return stocks that are predicted to increase or decreasse by more that 0.5%


## NB
Required Packages:  pandas_datareader, pandas, numpy, matplotlib, yfinance 
