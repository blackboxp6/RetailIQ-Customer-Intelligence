from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "online_retail_II.xlsx"
OUTPUT_PATH = BASE_DIR / "data" / "clean_transactions.parquet"

sheets = pd.read_excel(
    DATA_PATH,
    sheet_name=None,
    engine="openpyxl"
)

df = pd.concat(
    sheets.values(),
    ignore_index=True
)

df.columns = df.columns.str.strip()

df = df.rename(columns={
    "Invoice": "InvoiceNo",
    "Price": "UnitPrice",
    "Customer ID": "CustomerID"
})

print("Original records:", len(df))

# Remove exact duplicate rows
df = df.drop_duplicates()

# Remove records without customer identifiers
df = df.dropna(subset=["CustomerID"])

# Convert transaction dates
df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"],
    errors="coerce"
)

df = df.dropna(subset=["InvoiceDate"])

# Identify cancellations
df["InvoiceNo"] = df["InvoiceNo"].astype(str)

df["IsCancellation"] = (
    df["InvoiceNo"]
    .str.upper()
    .str.startswith("C")
)

# Keep positive purchase transactions
df = df[
    (~df["IsCancellation"])
    & (df["Quantity"] > 0)
    & (df["UnitPrice"] > 0)
].copy()

# Calculate transaction-line revenue
df["Revenue"] = (
    df["Quantity"] * df["UnitPrice"]
)

# Standardize customer identifiers
df["CustomerID"] = (
    df["CustomerID"]
    .astype(int)
    .astype(str)
)

# Standardize product identifiers
df["StockCode"] = (
    df["StockCode"]
    .astype("string")
    .str.strip()
)

# Standardize invoice identifiers
df["InvoiceNo"] = (
    df["InvoiceNo"]
    .astype("string")
    .str.strip()
)

# Standardize product descriptions
df["Description"] = (
    df["Description"]
    .astype("string")
    .str.strip()
)

df.to_parquet(
    OUTPUT_PATH,
    index=False
)

print("Clean records:", len(df))
print("Unique customers:", df["CustomerID"].nunique())
print("Total gross sales: £", round(df["Revenue"].sum(), 2))
print("Saved:", OUTPUT_PATH)