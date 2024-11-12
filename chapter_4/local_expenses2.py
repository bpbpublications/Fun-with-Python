import click
import pandas as pd
import matplotlib.pyplot as plt


class Expenser:
    def load_and_convert(self, file_path):
        self.df = pd.read_excel(file_path, sheet_name=None, header=None, names=("Type", "Value"))
        self.df["expenses"] = self.df["expenses"].sort_values("Value", ascending=False)
        print(self.df["expenses"])

    def draw(self):
        fig, ax = plt.subplots()

        ax.bar(self.df["expenses"]["Type"][:5], self.df["expenses"]["Value"][:5])

        ax.set_ylabel("amount ($)")
        ax.set_title("Results of expenses")
        ax.legend(title="Expenses")

        plt.show()


@click.command()
@click.option("--file", type=str, help="Data file", required=True)
def main(file):
    exp = Expenser()
    exp.load_and_convert(file)
    exp.draw()


if __name__ == "__main__":
    main()
