from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "customer_rfm.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

rfm = pd.read_csv(DATA_PATH)

print("Customer records:", len(rfm))
print(rfm.head())

features = ["Recency", "Frequency", "Monetary"]

X = rfm[features].copy()

# Verify input data
if X.isna().any().any():
    raise ValueError("RFM data contains missing values.")

if (X < 0).any().any():
    raise ValueError("RFM features must be nonnegative.")

# Log transformation
X_log = np.log1p(X)

# Standardization
scaler = StandardScaler()

X_scaled = scaler.fit_transform(X_log)

print("\nScaled feature means:")
print(X_scaled.mean(axis=0))

print("\nScaled feature standard deviations:")
print(X_scaled.std(axis=0))

k_values = range(2, 11)

inertias = []
silhouette_scores = []

for k in k_values:

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(X_scaled)

    inertia = model.inertia_

    score = silhouette_score(
        X_scaled,
        labels,
        sample_size=min(5000, len(X_scaled)),
        random_state=42
    )

    inertias.append(inertia)
    silhouette_scores.append(score)

    print(
        f"K={k} | "
        f"Inertia={inertia:.2f} | "
        f"Silhouette={score:.4f}"
    )

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

axes[0].plot(
    list(k_values),
    inertias,
    marker="o"
)

axes[0].set_title("Elbow Method")
axes[0].set_xlabel("Number of Clusters")
axes[0].set_ylabel("Inertia")
axes[0].grid(alpha=0.3)

axes[1].plot(
    list(k_values),
    silhouette_scores,
    marker="o"
)

axes[1].set_title("Silhouette Analysis")
axes[1].set_xlabel("Number of Clusters")
axes[1].set_ylabel("Silhouette Score")
axes[1].grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "cluster_evaluation.png",
    dpi=150
)

plt.show()

best_index = np.argmax(silhouette_scores)

best_k = 4

print(f"\nSelected number of clusters: {best_k}")

final_model = KMeans(
    n_clusters=best_k,
    random_state=42,
    n_init=10
)

rfm["Cluster"] = final_model.fit_predict(X_scaled)

print("\nCustomers per cluster:")
print(rfm["Cluster"].value_counts().sort_index())

cluster_profile = rfm.groupby("Cluster").agg(
    Customers=("CustomerID", "count"),
    Avg_Recency=("Recency", "mean"),
    Avg_Frequency=("Frequency", "mean"),
    Avg_Monetary=("Monetary", "mean"),
    Total_Revenue=("Monetary", "sum")
)

cluster_profile["Customer_Share"] = (
    cluster_profile["Customers"]
    / cluster_profile["Customers"].sum()
    * 100
)

cluster_profile["Revenue_Share"] = (
    cluster_profile["Total_Revenue"]
    / cluster_profile["Total_Revenue"].sum()
    * 100
)

print("\nCUSTOMER SEGMENT PROFILES")
print(cluster_profile.round(2))

cluster_profile.to_csv(
    OUTPUT_DIR / "cluster_profiles.csv"
)

rfm.to_csv(
    OUTPUT_DIR / "customer_segments.csv",
    index=False
)

from sklearn.decomposition import PCA

pca = PCA(n_components=2)

X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(10, 7))

for cluster in sorted(rfm["Cluster"].unique()):

    mask = rfm["Cluster"] == cluster

    plt.scatter(
        X_pca[mask, 0],
        X_pca[mask, 1],
        label=f"Cluster {cluster}",
        alpha=0.45,
        s=15
    )

plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")

plt.title("RetailIQ — Customer Segmentation")

plt.legend(title="Customer Segment")
plt.grid(alpha=0.2)

plt.tight_layout()
plt.show()

print(
    "\nPCA explained variance:",
    pca.explained_variance_ratio_
)

# Calculate average RFM values per cluster
profile = rfm.groupby("Cluster")[
    ["Recency", "Frequency", "Monetary"]
].mean()

print("\nAVERAGE CUSTOMER BEHAVIOR")
print(profile.round(2))

# Compare clusters against the overall customer population
overall = rfm[
    ["Recency", "Frequency", "Monetary"]
].mean()

relative_profile = profile.div(overall)

print("\nRELATIVE CUSTOMER BEHAVIOR")
print(relative_profile.round(2))

loadings = pd.DataFrame(
    pca.components_.T,
    index=["Recency", "Frequency", "Monetary"],
    columns=["PC1", "PC2"]
)

print("\nPCA LOADINGS")
print(loadings.round(3))

print("\nEXPLAINED VARIANCE")
print(pca.explained_variance_ratio_)

print("\nTOTAL EXPLAINED VARIANCE")
print(pca.explained_variance_ratio_.sum())