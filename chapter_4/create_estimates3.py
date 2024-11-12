import click
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from seed_example_data import EXPENSES


class Interpolation:
    def __init__(self, source_file):
        self.df = pd.read_excel(source_file, sheet_name=None, header=None, names=("Date", "Value"))
        self.df_origin = pd.read_excel(source_file, sheet_name=None, names=("Date", "Value"), index_col=1)

    def aggregate(self):
        values = []
        for expense in EXPENSES:
            self.df[expense]["Date"] = pd.to_datetime(self.df[expense]["Date"].loc[1:]) - pd.to_timedelta(7, unit="d")
            self.df[expense] = self.df[expense].groupby([pd.Grouper(key="Date", freq="W")])["Value"].sum()
            values.append((expense, self.df[expense].sum()))

        self.df_most = pd.DataFrame(values, columns=("Type", "Value"), index=EXPENSES)
        self.df_most.sort_values("Value", ascending=False)

    def get_most_expenses(self):
        return list(self.df_most[:5].index)

    def predict(self):
        for key in self.get_most_expenses():
            df = self.df_origin[key]
            df = df.drop(df.columns[0], axis=1)
            self.prepare_estimate(df)

    def prepare_estimate(self, df):
        forecast_col = "Value"
        df.fillna(value=-99999, inplace=True)
        forecast_size = int(math.ceil(0.03 * len(df)))

        df["label"] = df[forecast_col].shift(-forecast_size)

        x = np.array(df.drop(["label"], axis=1))
        x = preprocessing.power_transform(x)
        x_lately = x[-forecast_size:]
        x = x[:-forecast_size]

        df.dropna(inplace=True)

        y = np.array(df["label"])
        x_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
        clf = Ridge(alpha=1.0)
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

        df[forecast_col].plot()
        df["Forecast"].plot()

    def plot(self):
        plt.legend(loc=4)
        plt.ylabel("Value")
        plt.xlabel("Date")
        plt.show()


@click.command()
@click.option("--source", type=str, help="Source file to load", required=True)
def main(source):
    i = Interpolation(source)
    i.aggregate()
    i.get_most_expenses()
    i.predict()
    i.plot()


if __name__ == "__main__":
    main()
