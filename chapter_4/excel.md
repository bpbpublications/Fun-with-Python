# csv

## pandas

```bash
$ pip install pandas
```
# install

```bash
$ pip install matplotlib click openpyxl
```

# import

## from XLS

```python
import click
import pandas as pd

class Expenser:
    def load_and_convert(self, file_path):
        self.df = pd.read_excel(file_path, sheet_name=None, header=None, names=('Type', 'Value'))
        print(self.df['expenses'])

@click.command()
@click.option("--file", type=str, help="Data file", required=True)
def main(file):
    exp = Expenser()
    exp.load_and_convert(file)

if __name__ == '__main__':
    main()
```

# load expenses

```bash
$ python load_expenses.py --file expense-example.xlsx
```
