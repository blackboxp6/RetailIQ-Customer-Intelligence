from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_parquet(
    BASE_DIR / "data" / "clean_transactions.parquet"
)

# Define the analysis reference date
snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

# Calculate RFM
rfm = df.groupby("CustomerID").agg(
    LastPurchase=("InvoiceDate", "max"),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("Revenue", "sum")
)

# Days since last purchase
rfm["Recency"] = (
    snapshot_date - rfm["LastPurchase"]
).dt.days

rfm = rfm[
    ["Recency", "Frequency", "Monetary"]
]

print("\nRFM Summary:")
print(rfm.describe())

print("\nTop Customers:")
print(
    rfm.sort_values(
        "Monetary",
        ascending=False
    ).head(10)
)

output = BASE_DIR / "data" / "customer_rfm.csv"

rfm.to_csv(output)

print("\nSaved:", output)