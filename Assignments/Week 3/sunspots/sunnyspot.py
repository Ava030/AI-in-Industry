import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose

df = pd.read_csv('Sunspots.csv')

# Seasonal decomposition
result = seasonal_decompose(
    df['Monthly Mean Total Sunspot Number'], model='additive', period=12)
result.plot()
plt.show()

# ACF and PACF plots
plot_acf(df['Monthly Mean Total Sunspot Number'], lags=40)
plot_pacf(df['Monthly Mean Total Sunspot Number'], lags=40)
plt.show()

# SARIMA model
model = SARIMAX(df['Monthly Mean Total Sunspot Number'],
                order=(1, 0, 1), seasonal_order=(1, 1, 1, 12))
results = model.fit()

# Predict
df['forecast'] = results.predict(
    start=pd.to_datetime('1749-01-31'), dynamic=False)
df[['Monthly Mean Total Sunspot Number', 'forecast']].plot(figsize=(12, 8))
plt.show()
