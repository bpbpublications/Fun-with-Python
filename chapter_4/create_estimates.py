import click
import pandas as pd
import matplotlib.pyplot as plt
from seed_example_data import EXPENSES


class Interpolation:
    def __init__(self, source_file):
        self.df = pd.read_excel(source_file, sheet_name=None, header=None, names=("Date", "Value"))

    def aggregate(self):
        for expense in EXPENSES:
            self.df[expense]["Date"] = pd.to_datetime(self.df[expense]["Date"][1:]) - pd.to_timedelta(7, unit="d")
            self.df[expense] = self.df[expense].groupby([pd.Grouper(key="Date", freq="W")])["Value"].sum()
        print(self.df)

    def plot(self):
        for expense in EXPENSES:
            self.df[expense].plot(label=expense, legend=True)
        plt.legend(loc=4)
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.show()


@click.command()
@click.option("--source", type=str, help="Source file to load", required=True)
def main(source):
    i = Interpolation(source)
    i.aggregate()
    i.plot()


if __name__ == "__main__":
    main()
