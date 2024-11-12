import pandas as pd

# specify the path of the Excel file
excel_file = "example.xlsx"
# read the Excel file into a pandas DataFrame
df = pd.read_excel(excel_file)
print(df.head())
