# ============================================================
# EEG FEATURE ANALYSIS
# ============================================================
# Purpose:
# 1. Analyze feature correlations
# 2. Detect highly redundant features
# 3. Calculate Extra Trees feature importance
# 4. Calculate Mutual Information
# 5. Generate class-wise feature statistics
# 6. Save analysis results and plots
#
# Dataset:
# dataset\EEG_Extracted_Features(1).csv
#
# Output:
# results\feature_analysis\
# ============================================================


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import mutual_info_classif
from sklearn.ensemble import ExtraTreesClassifier


# ============================================================
# 1. PATHS
# ============================================================

INPUT_FILE = r"dataset\EEG_Extracted_Features.csv"

OUTPUT_DIR = r"results\feature_analysis"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# 2. LOAD DATA
# ============================================================

print("\n" + "=" * 70)
print("EEG FEATURE ANALYSIS")
print("=" * 70)

print("\nLoading dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Dataset shape: {df.shape}")


# ============================================================
# 3. BASIC DATA INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("DATASET INFORMATION")
print("=" * 70)

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nClass distribution:")
print(df["Label"].value_counts())


# ============================================================
# 4. SEPARATE FEATURES AND LABEL
# ============================================================

X = df.drop("Label", axis=1)

label_encoder = LabelEncoder()

y = label_encoder.fit_transform(df["Label"])

feature_names = X.columns.tolist()


# ============================================================
# 5. CORRELATION ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("FEATURE CORRELATION ANALYSIS")
print("=" * 70)

correlation_matrix = X.corr()

print("\nCorrelation Matrix:")
print(correlation_matrix.round(3).to_string())


# Save correlation matrix
correlation_matrix.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "correlation_matrix.csv"
    )
)


# ============================================================
# 6. FIND HIGHLY CORRELATED FEATURE PAIRS
# ============================================================

print("\n" + "=" * 70)
print("HIGHLY CORRELATED FEATURE PAIRS")
print("=" * 70)

correlation_pairs = []

for i in range(len(feature_names)):

    for j in range(i + 1, len(feature_names)):

        feature_1 = feature_names[i]
        feature_2 = feature_names[j]

        correlation = correlation_matrix.loc[
            feature_1,
            feature_2
        ]

        if abs(correlation) >= 0.90:

            correlation_pairs.append({
                "Feature_1": feature_1,
                "Feature_2": feature_2,
                "Correlation": correlation,
                "Absolute_Correlation": abs(correlation)
            })


correlation_pairs_df = pd.DataFrame(
    correlation_pairs
)


if len(correlation_pairs_df) > 0:

    correlation_pairs_df = correlation_pairs_df.sort_values(
        "Absolute_Correlation",
        ascending=False
    )

    print(
        correlation_pairs_df.to_string(index=False)
    )

else:

    print("\nNo feature pairs with |correlation| >= 0.90 found.")


# Save
correlation_pairs_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "high_correlation_pairs.csv"
    ),
    index=False
)


# ============================================================
# 7. CORRELATION HEATMAP
# ============================================================

print("\nGenerating correlation heatmap...")

plt.figure(
    figsize=(14, 11)
)

plt.imshow(
    correlation_matrix,
    interpolation="nearest",
    aspect="auto"
)

plt.colorbar()

plt.xticks(
    range(len(feature_names)),
    feature_names,
    rotation=90
)

plt.yticks(
    range(len(feature_names)),
    feature_names
)

plt.title(
    "EEG Feature Correlation Matrix"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "correlation_heatmap.png"
    ),
    dpi=300
)

plt.close()


# ============================================================
# 8. EXTRA TREES FEATURE IMPORTANCE
# ============================================================

print("\n" + "=" * 70)
print("EXTRA TREES FEATURE IMPORTANCE")
print("=" * 70)

extra_trees = ExtraTreesClassifier(
    n_estimators=500,
    random_state=42,
    n_jobs=-1
)

extra_trees.fit(
    X,
    y
)

importance = extra_trees.feature_importances_


importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importance
})


importance_df = importance_df.sort_values(
    "Importance",
    ascending=False
)


print("\nFeature importance ranking:")
print(
    importance_df.to_string(index=False)
)


# Save
importance_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "extra_trees_feature_importance.csv"
    ),
    index=False
)


# ============================================================
# 9. EXTRA TREES IMPORTANCE PLOT
# ============================================================

print("\nGenerating Extra Trees importance plot...")

plot_df = importance_df.sort_values(
    "Importance",
    ascending=True
)

plt.figure(
    figsize=(10, 8)
)

plt.barh(
    plot_df["Feature"],
    plot_df["Importance"]
)

plt.xlabel(
    "Feature Importance"
)

plt.ylabel(
    "Feature"
)

plt.title(
    "Extra Trees Feature Importance"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "extra_trees_feature_importance.png"
    ),
    dpi=300
)

plt.close()


# ============================================================
# 10. MUTUAL INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("MUTUAL INFORMATION")
print("=" * 70)

mi_scores = mutual_info_classif(
    X,
    y,
    random_state=42
)


mi_df = pd.DataFrame({
    "Feature": feature_names,
    "Mutual_Information": mi_scores
})


mi_df = mi_df.sort_values(
    "Mutual_Information",
    ascending=False
)


print("\nMutual Information ranking:")
print(
    mi_df.to_string(index=False)
)


# Save
mi_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "mutual_information.csv"
    ),
    index=False
)


# ============================================================
# 11. MUTUAL INFORMATION PLOT
# ============================================================

print("\nGenerating Mutual Information plot...")

plot_df = mi_df.sort_values(
    "Mutual_Information",
    ascending=True
)

plt.figure(
    figsize=(10, 8)
)

plt.barh(
    plot_df["Feature"],
    plot_df["Mutual_Information"]
)

plt.xlabel(
    "Mutual Information"
)

plt.ylabel(
    "Feature"
)

plt.title(
    "EEG Feature Mutual Information"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "mutual_information.png"
    ),
    dpi=300
)

plt.close()


# ============================================================
# 12. CLASS-WISE MEAN
# ============================================================

print("\n" + "=" * 70)
print("CLASS-WISE FEATURE MEANS")
print("=" * 70)

class_means = df.groupby(
    "Label"
)[feature_names].mean()


print("\nClass-wise means:")
print(
    class_means.round(4).to_string()
)


class_means.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "class_wise_means.csv"
    )
)


# ============================================================
# 13. CLASS-WISE STANDARD DEVIATION
# ============================================================

print("\n" + "=" * 70)
print("CLASS-WISE FEATURE STANDARD DEVIATION")
print("=" * 70)

class_std = df.groupby(
    "Label"
)[feature_names].std()


print("\nClass-wise standard deviation:")
print(
    class_std.round(4).to_string()
)


class_std.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "class_wise_std.csv"
    )
)


# ============================================================
# 14. TOP FEATURES SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("TOP FEATURES SUMMARY")
print("=" * 70)


top_importance = importance_df.head(10)

top_mi = mi_df.head(10)


print("\nTop 10 Extra Trees features:")
print(
    top_importance.to_string(index=False)
)


print("\nTop 10 Mutual Information features:")
print(
    top_mi.to_string(index=False)
)


# ============================================================
# 15. COMBINED FEATURE RANKING
# ============================================================

print("\n" + "=" * 70)
print("COMBINED FEATURE ANALYSIS")
print("=" * 70)

combined_df = pd.merge(
    importance_df,
    mi_df,
    on="Feature"
)

combined_df["Importance_Rank"] = (
    combined_df["Importance"]
    .rank(
        ascending=False,
        method="min"
    )
)

combined_df["MI_Rank"] = (
    combined_df["Mutual_Information"]
    .rank(
        ascending=False,
        method="min"
    )
)

combined_df["Average_Rank"] = (
    combined_df["Importance_Rank"]
    +
    combined_df["MI_Rank"]
) / 2


combined_df = combined_df.sort_values(
    "Average_Rank"
)


print(
    combined_df.round(5).to_string(index=False)
)


combined_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "combined_feature_ranking.csv"
    ),
    index=False
)


# ============================================================
# 16. FINAL SUMMARY FILE
# ============================================================

summary_file = os.path.join(
    OUTPUT_DIR,
    "analysis_summary.txt"
)


with open(
    summary_file,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "EEG FEATURE ANALYSIS SUMMARY\n"
    )

    f.write(
        "=" * 50 + "\n\n"
    )

    f.write(
        f"Dataset shape: {df.shape}\n"
    )

    f.write(
        f"Number of features: {len(feature_names)}\n"
    )

    f.write(
        f"Number of classes: {df['Label'].nunique()}\n"
    )

    f.write(
        f"Missing values: {df.isnull().sum().sum()}\n"
    )

    f.write(
        f"Duplicate rows: {df.duplicated().sum()}\n\n"
    )

    f.write(
        "Top Extra Trees Features:\n"
    )

    for _, row in importance_df.head(10).iterrows():

        f.write(
            f"{row['Feature']}: "
            f"{row['Importance']:.6f}\n"
        )

    f.write(
        "\nTop Mutual Information Features:\n"
    )

    for _, row in mi_df.head(10).iterrows():

        f.write(
            f"{row['Feature']}: "
            f"{row['Mutual_Information']:.6f}\n"
        )

    f.write(
        "\nHighly Correlated Feature Pairs "
        "(absolute correlation >= 0.90):\n"
    )

    if len(correlation_pairs_df) > 0:

        for _, row in correlation_pairs_df.iterrows():

            f.write(
                f"{row['Feature_1']} <-> "
                f"{row['Feature_2']}: "
                f"{row['Correlation']:.6f}\n"
            )

    else:

        f.write(
            "None found.\n"
        )


# ============================================================
# 17. FINISHED
# ============================================================

print("\n" + "=" * 70)
print("FEATURE ANALYSIS COMPLETED")
print("=" * 70)

print("\nAll results saved in:")

print(
    OUTPUT_DIR
)

print("\nGenerated files:")

for filename in sorted(
    os.listdir(OUTPUT_DIR)
):

    print(
        " -",
        filename
    )

print("\nDone.")