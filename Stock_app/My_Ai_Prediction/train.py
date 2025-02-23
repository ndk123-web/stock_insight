import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import datetime

# --- 1. Fetch intraday stock data using yfinance ---
symbol = "AAPL"  # Example stock symbol (Apple Inc.)
# Download intraday data for 1 day with 5-minute interval
data = yf.download(tickers=symbol, period="1d", interval="5m")

if data.empty:
    print(f"No data found for {symbol}")
    exit()

# --- 2. Extract timestamps and "Open" prices ---
# The index contains timestamps (as pandas Timestamp objects)
time_stamps = data.index  
open_prices = data['Open'].values

# --- 3. Convert timestamps to numeric values ---
# For regression, we convert each timestamp to minutes elapsed since the first timestamp.
base_time = time_stamps[0]
x_numeric = np.array([(ts - base_time).total_seconds() / 60 for ts in time_stamps]).reshape(-1, 1)

# Convert the open prices list to a numpy array
y_array = np.array(open_prices)

# --- 4. Fit a polynomial regression model (degree=2) ---
poly = PolynomialFeatures(degree=2)
x_poly = poly.fit_transform(x_numeric)
model = LinearRegression()
model.fit(x_poly, y_array)

# Generate a smooth line for predictions
x_new = np.linspace(x_numeric.min(), x_numeric.max(), 100).reshape(-1, 1)
x_new_poly = poly.transform(x_new)
y_pred = model.predict(x_new_poly)
