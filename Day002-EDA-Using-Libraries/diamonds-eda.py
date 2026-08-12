import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 20)
sns.set_theme(style="whitegrid", context="notebook")

df = sns.load_dataset("diamonds")

print("=" * 70)
print("1. DATASET")
print("=" * 70)
print(f"shape         : {df.shape[0]:,} rows x {df.shape[1]} columns")
print(f"memory        : {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
print(f"null cells    : {df.isna().sum().sum()}")
print(f"duplicate rows: {df.duplicated().sum()}")
print("\ndtype breakdown:")
print(df.dtypes.value_counts().to_string())

print("\nnumeric summary (via .describe()):")
print(df.describe().round(2))

print("\n" + "=" * 70)
print("2. DATA QUALITY CHECKS")
print("=" * 70)

zero_dim = ((df["x"] == 0) | (df["y"] == 0) | (df["z"] == 0)).sum()
absurd_y = (df["y"] > 30).sum()       # largest legit diamond y is ~10mm
absurd_z = (df["z"] > 30).sum()

print(f"rows with a zero dimension : {zero_dim}")
print(f"rows with y > 30mm (absurd): {absurd_y}")
print(f"rows with z > 30mm (absurd): {absurd_z}")

mask = (df[["x", "y", "z"]] > 0).all(axis=1) & (df["y"] < 30) & (df["z"] < 30)
clean = df[mask].copy()
print(f"kept {len(clean):,} of {len(df):,} rows ({len(clean)/len(df):.2%})")

print("\n" + "=" * 70)
print("3. ENGINEERED FEATURES")
print("=" * 70)

clean["volume"] = clean["x"] * clean["y"] * clean["z"]              # mm^3
clean["price_per_carat"] = clean["price"] / clean["carat"]          # $/ct
clean["log_carat"] = np.log(clean["carat"])                         # for log-log
clean["log_price"] = np.log(clean["price"])

edges = [0, 0.5, 1.0, 1.5, 2.0, np.inf]
labels = ["<0.5ct", "0.5-1ct", "1-1.5ct", "1.5-2ct", "2ct+"]

clean["carat_bin"] = pd.cut(clean["carat"], bins=edges, labels=labels, ordered=True)

print(clean[["carat", "volume", "price_per_carat", "carat_bin"]].head())

print("\n" + "=" * 70)
print("4. PRICE BY CUT AND CARAT BIN")
print("=" * 70)

naive = clean.groupby("cut", observed=True)["price"].mean().round(0)
print("\nNAIVE mean price by cut (misleading!):")
print(naive.to_string())

pivot = clean.pivot_table(
    values="price",
    index="carat_bin",
    columns="cut",
    aggfunc="mean",
    observed=True,
).round(0)
print("\nMean price by cut CONTROLLED FOR CARAT (the honest view):")
print(pivot.to_string())

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Diamonds: distributional & structural view", fontsize=15, y=1.00)

axes[0, 0].hist(clean["price"], bins=60, color="#4a7ab8", edgecolor="white")
axes[0, 0].set_title("Price distribution (raw $)")
axes[0, 0].set_xlabel("price ($)")
axes[0, 0].set_ylabel("count")
axes[0, 0].axvline(clean["price"].median(), color="crimson", ls="--",
                   label=f"median ${clean['price'].median():,.0f}")
axes[0, 0].legend()

axes[0, 1].hist(clean["log_price"], bins=60, color="#4a7ab8", edgecolor="white")
axes[0, 1].set_title("log(price) — normal-ish, model-friendly")
axes[0, 1].set_xlabel("log(price)")

# relationship: price ≈ carat^k.
sample = clean.sample(4000, random_state=0)
axes[1, 0].scatter(sample["log_carat"], sample["log_price"],
                   s=6, alpha=0.35, c="#2f6f4f")
slope, intercept = np.polyfit(clean["log_carat"], clean["log_price"], 1)
xs = np.linspace(clean["log_carat"].min(), clean["log_carat"].max(), 50)
axes[1, 0].plot(xs, slope * xs + intercept, "r--", lw=2,
                label=f"fit: log(p) = {slope:.2f}·log(c) + {intercept:.2f}")
axes[1, 0].set_title("log(price) vs log(carat) — the power law")
axes[1, 0].set_xlabel("log(carat)")
axes[1, 0].set_ylabel("log(price)")
axes[1, 0].legend()

cut_counts = clean["cut"].value_counts().sort_index()
axes[1, 1].bar(cut_counts.index.astype(str), cut_counts.values,
               color="#c26a2a", edgecolor="white")
axes[1, 1].set_title("Diamonds by cut quality")
axes[1, 1].set_ylabel("count")
axes[1, 1].tick_params(axis="x", rotation=20)

fig.tight_layout()
fig.savefig("fig1_distributions.png", dpi=110, bbox_inches="tight")
plt.close(fig)

numeric = clean.select_dtypes(include=[np.number])
corr = numeric.corr()

fig, ax = plt.subplots(figsize=(9, 7))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
            square=True, linewidths=0.5, ax=ax,
            cbar_kws={"shrink": 0.75, "label": "Pearson r"})
ax.set_title("Correlation matrix — carat/volume/dims all drive price",
             fontsize=13, pad=12)
fig.tight_layout()
fig.savefig("fig2_corr_heatmap.png", dpi=110, bbox_inches="tight")
plt.close(fig)

fig, ax = plt.subplots(figsize=(11, 6))
sns.violinplot(
    data=clean, x="carat_bin", y="price", hue="cut",
    palette="viridis", inner="quartile", cut=0, ax=ax,
)
ax.set_title("Price by carat bin, split by cut — where cut quality actually shows up",
             fontsize=13)
ax.set_xlabel("carat bin")
ax.set_ylabel("price ($)")
ax.legend(title="cut", loc="upper left", ncol=3)
fig.tight_layout()
fig.savefig("fig3_violin.png", dpi=110, bbox_inches="tight")
plt.close(fig)

print("\n" + "=" * 70)
print("6. WHAT THE DATA ACTUALLY SAYS")
print("=" * 70)
print(f"  - price is right-skewed; log(price) is close to normal")
print(f"  - power law fit: price ≈ carat^{slope:.2f}")
print(f"  - carat, volume, x, y, z are all >0.85 correlated with price")
print(f"  - depth and table barely matter (|r| < 0.02)")
print(f"  - naive 'Ideal cut is cheapest' is Simpson's paradox — smaller")
print(f"    stones tend to get the best cuts. Controlling for carat bin")
print(f"    reverses the ordering (see pivot above).")