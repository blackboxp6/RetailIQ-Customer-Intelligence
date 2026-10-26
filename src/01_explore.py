from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "online_retail_II.xlsx"

print("Loading RetailIQ dataset...")

# Read both Excel worksheets
sheets = pd.read_excel(
    DATA_PATH,
    sheet_name=None,
    engine="openpyxl"
)

df = pd.concat(
    sheets.values(),
    ignore_index=True
)

# Standardize column names
df.columns = df.columns.str.strip()

df = df.rename(columns={
    "Invoice": "InvoiceNo",
    "Price": "UnitPrice",
    "Customer ID": "CustomerID"
})

print("\nDataset shape:")
print(df.shape)

print("\nFirst five transactions:")
print(df.head())

print("\nColumn information:")
print(df.info())

print("\nMissing values:")
print(df.isnull().sum())

print("\nStatistical summary:")
print(df.describe())

print("\nDate range:")
print(df["InvoiceDate"].min())
print(df["InvoiceDate"].max())

print("\nUnique customers:")
print(df["CustomerID"].nunique())

print("\nUnique products:")
print(df["StockCode"].nunique())