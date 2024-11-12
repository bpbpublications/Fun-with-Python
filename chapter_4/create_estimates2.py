import click
import pandas as pd
import matplotlib.pyplot as plt
from seed_example_data import EXPENSES


class Interpolation:
    def __init__(self, source_file):
        self.df = pd.read_excel(source_file, sheet_name=None, header=None, names=("Date", "Value"))

    def aggregate(self):
        values = []
        for expense in EXPENSES:
            self.df[expense]["Date"] = pd.to_datetime(self.df[expense]["Date"][1:]) - pd.to_timedelta(7, unit="d")
            self.df[expense] = self.df[expense].groupby([pd.Grouper(key="Date", freq="W")])["Value"].sum()
            values.append((expense, self.df[expense].sum()))

        self.df_most = pd.DataFrame(values, columns=("Type", "Value"), index=EXPENSES)
        self.df_most.sort_values("Value", ascending=False)

    def plot(self):
        ax = self.df_most[:5].plot.bar(rot=0)
        for container in ax.containers:
            ax.bar_label(container)
        plt.xlabel("Type")
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
