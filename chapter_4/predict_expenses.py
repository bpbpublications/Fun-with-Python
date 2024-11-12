import random
from datetime import datetime

import quandl, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from matplotlib import style

style.use("ggplot")

df = quandl.get("WIKI/GOOGL")
df = df[["Adj. Open", "Adj. High", "Adj. Low", "Adj. Close", "Adj. Volume"]]
df = df[["Adj. Close", "Adj. Volume"]]

forecast_col = "Adj. Close"
df.fillna(value=-99999, inplace=True)
forecast_size = int(math.ceil(0.02 * len(df)))
print("Forecast size: {forecast_size}")

df["label"] = df[forecast_col].shift(-forecast_size)

x = np.array(df.drop(["label"], axis=1))
x = preprocessing.scale(x)
x_lately = x[-forecast_size:]
x = x[:-forecast_size]

df.dropna(inplace=True)

y = np.array(df["label"])
x_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
clf = LinearRegression(n_jobs=-1)
clf.fit(x_train, y_train)
confidence = clf.score(X_test, y_test)

forecast_set = clf.predict(x_lately)
df["Forecast"] = np.nan
last_date = df.iloc[-1].name
last_unix = last_date.timestamp()
one_day = 24 * 60 * 60  # 1 day in seconds
next_unix = last_unix + one_day

for i in forecast_set:
    next_date = datetime.fromtimestamp(next_unix)
    next_unix += one_day
    df.loc[next_date] = [np.nan for _ in range(len(df.columns) - 1)] + [i]

df["Adj. Close"].plot()
df["Forecast"].plot()
plt.legend(loc=4)
plt.ylabel("Value")
plt.xlabel("Date")
plt.show()
