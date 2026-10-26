from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    BASE_DIR / "outputs" / "business_analysis.csv"
)

segment_names = {
    0: "Dormant",
    1: "Developing",
    2: "High Value",
    3: "Lapsing"
}

df["Segment"] = df["Cluster"].map(segment_names)

x = np.arange(len(df))
width = 0.35

fig, ax = plt.subplots(figsize=(11, 6))

bars1 = ax.bar(
    x - width / 2,
    df["Customer_Share"],
    width,
    label="Customer Share"
)

bars2 = ax.bar(
    x + width / 2,
    df["Revenue_Share"],
    width,
    label="Revenue Share"
)

ax.set_xticks(x)
ax.set_xticklabels(df["Segment"])

ax.set_ylabel("Percentage (%)")
ax.set_title(
    "RetailIQ — Customer Share vs Revenue Contribution"
)

ax.legend()
ax.grid(axis="y", alpha=0.2)

ax.bar_label(bars1, fmt="%.1f%%", padding=3)
ax.bar_label(bars2, fmt="%.1f%%", padding=3)

plt.tight_layout()

plt.savefig(
    BASE_DIR / "outputs" / "segment_revenue_comparison.png",
    dpi=150
)

plt.show()