import yfinance as yf
import pandas as pd
import statsmodels.api as sm
from datetime import date
import getFamaFrenchFactors as gff


# Replace 'AAPL' with your asset's ticker
ticker = "msft"
stock = yf.Ticker(ticker)

# Get option chain for specific expiration
opt = stock.option_chain()  # Use a specific expiration date

# Accessing calls and puts
calls = opt.calls
puts = opt.puts

implied_volatility = (float(calls.impliedVolatility.mean())*len(calls) + len(calls)*float(puts.impliedVolatility.mean()))/(len(puts)+len(calls))

start = '2016-8-31'
end = date.today()

stock_data = yf.download(ticker, start, end)

ff3_monthly = gff.famaFrench3Factor(frequency='m')
ff3_monthly.rename(columns={"date_ff_factors": 'Date'}, inplace=True)
ff3_monthly.set_index('Date', inplace=True)

stock_returns = stock_data['Adj Close'].resample('M').last().pct_change().dropna()
stock_returns.name = "Month_Rtn"
ff_data = ff3_monthly.merge(stock_returns,on='Date')

X = ff_data[['Mkt-RF', 'SMB', 'HML']]
y = ff_data['Month_Rtn'] - ff_data['RF']
X = sm.add_constant(X)
ff_model = sm.OLS(y, X).fit()
#print(ff_model.summary())
intercept, b1, b2, b3 = ff_model.params

rf = ff_data['RF'].mean()
market_premium = ff3_monthly['Mkt-RF'].mean()
size_premium = ff3_monthly['SMB'].mean()
value_premium = ff3_monthly['HML'].mean()

expected_monthly_return = rf + b1 * market_premium + b2 * size_premium + b3 * value_premium 
expected_yearly_return = expected_monthly_return * 12
print("Expected yearly return: " + str(expected_yearly_return))
print("Expected yearly variance: " + str(implied_volatility))