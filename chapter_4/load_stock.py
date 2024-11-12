import math
import quandl

df = quandl.get("WIKI/GOOGL")
df = df[["Adj. Open", "Adj. High", "Adj. Low", "Adj. Close", "Adj. Volume"]]

df = df[["Adj. Close", "Adj. Volume"]]

forecast_column = "Adj. Close"
df.fillna(value=-99999, inplace=True)
forecast_outcome = int(math.ceil(0.01 * len(df)))

df["forecast_label"] = df[forecast_column].shift(-forecast_outcome)

print(df)
