from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    BASE_DIR / "outputs" / "customer_segments.csv"
)

summary = df.groupby("Cluster").agg(
    Customers=("CustomerID", "count"),
    Total_Revenue=("Monetary", "sum"),
    Average_Spending=("Monetary", "mean"),
    Average_Frequency=("Frequency", "mean"),
    Average_Recency=("Recency", "mean")
)

summary["Customer_Share"] = (
    summary["Customers"]
    / summary["Customers"].sum()
    * 100
)

summary["Revenue_Share"] = (
    summary["Total_Revenue"]
    / summary["Total_Revenue"].sum()
    * 100
)

summary["Revenue_Per_Customer"] = (
    summary["Total_Revenue"]
    / summary["Customers"]
)

print("\nRETAILIQ BUSINESS ANALYSIS")
print(summary.round(2).to_string())

summary.to_csv(
    BASE_DIR / "outputs" / "business_analysis.csv"
)