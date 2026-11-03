# ============================================================
# EEG LEAKAGE-SAFE FEATURE SELECTION + CROSS VALIDATION
# ============================================================

import os
import pandas as pd
import numpy as np

from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import make_scorer, accuracy_score


# ============================================================
# 1. PATHS
# ============================================================

INPUT_FILE = r"dataset\EEG_Extracted_Features.csv"

OUTPUT_DIR = r"results\feature_selection_cv"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# 2. LOAD DATA
# ============================================================

print("\n" + "=" * 70)
print("EEG LEAKAGE-SAFE FEATURE SELECTION")
print("=" * 70)

print("\nLoading dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Dataset shape: {df.shape}")


# ============================================================
# 3. PREPARE DATA
# ============================================================

X = df.drop("Label", axis=1)
y = df["Label"]

print(f"Number of features: {X.shape[1]}")
print(f"Number of samples: {X.shape[0]}")
print(f"Number of classes: {y.nunique()}")


# ============================================================
# 4. CROSS-VALIDATION
# ============================================================

cv = StratifiedKFold(
    n_splits=10,
    shuffle=True,
    random_state=42
)


# ============================================================
# 5. FEATURE SELECTION MODEL
# ============================================================
#
# IMPORTANT:
# SelectFromModel is INSIDE the Pipeline.
#
# Therefore feature selection is performed separately
# inside every training fold.
#
# This prevents data leakage.
# ============================================================

feature_selector = SelectFromModel(
    estimator=ExtraTreesClassifier(
        n_estimators=500,
        random_state=42,
        n_jobs=-1
    ),
    threshold="median"
)


# ============================================================
# 6. FINAL MODEL
# ============================================================

classifier = ExtraTreesClassifier(
    n_estimators=500,
    random_state=42,
    n_jobs=-1
)


# ============================================================
# 7. PIPELINE
# ============================================================

pipeline = Pipeline([
    (
        "feature_selection",
        feature_selector
    ),
    (
        "classifier",
        classifier
    )
])


# ============================================================
# 8. CROSS-VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("RUNNING 10-FOLD LEAKAGE-SAFE CROSS-VALIDATION")
print("=" * 70)

scores = cross_val_score(
    pipeline,
    X,
    y,
    cv=cv,
    scoring="accuracy",
    n_jobs=-1
)


# ============================================================
# 9. PRINT FOLD RESULTS
# ============================================================

print("\nFold Accuracies:")

for i, score in enumerate(scores, start=1):

    print(
        f"Fold {i:2d}: {score * 100:.2f}%"
    )


# ============================================================
# 10. STATISTICS
# ============================================================

mean_accuracy = scores.mean() * 100
std_accuracy = scores.std() * 100

print("\n" + "=" * 70)
print("FINAL CROSS-VALIDATION RESULTS")
print("=" * 70)

print(
    f"\nMean Accuracy : {mean_accuracy:.2f}%"
)

print(
    f"Std Deviation : {std_accuracy:.2f}%"
)

print(
    f"Minimum Fold  : {scores.min() * 100:.2f}%"
)

print(
    f"Maximum Fold  : {scores.max() * 100:.2f}%"
)


# ============================================================
# 11. SAVE FOLD RESULTS
# ============================================================

fold_results = pd.DataFrame({
    "Fold": range(1, len(scores) + 1),
    "Accuracy": scores * 100
})


fold_results.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "feature_selection_cv_folds.csv"
    ),
    index=False
)


# ============================================================
# 12. SAVE SUMMARY
# ============================================================

summary = pd.DataFrame({
    "Metric": [
        "Mean Accuracy",
        "Standard Deviation",
        "Minimum Fold Accuracy",
        "Maximum Fold Accuracy"
    ],
    "Value": [
        mean_accuracy,
        std_accuracy,
        scores.min() * 100,
        scores.max() * 100
    ]
})


summary.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "feature_selection_cv_summary.csv"
    ),
    index=False
)


# ============================================================
# 13. FIT ON FULL DATA ONLY FOR FEATURE INSPECTION
# ============================================================
#
# This section is ONLY for understanding which features
# are selected by the final fitted selector.
#
# It is NOT used to calculate CV accuracy.
# ============================================================

print("\n" + "=" * 70)
print("FEATURE SELECTION INSPECTION")
print("=" * 70)

pipeline.fit(
    X,
    y
)


selector = pipeline.named_steps[
    "feature_selection"
]

selected_mask = selector.get_support()

selected_features = X.columns[
    selected_mask
].tolist()

removed_features = X.columns[
    ~selected_mask
].tolist()


print(
    f"\nOriginal features : {X.shape[1]}"
)

print(
    f"Selected features : {len(selected_features)}"
)

print(
    f"Removed features  : {len(removed_features)}"
)


print("\nSelected Features:")

for feature in selected_features:

    print(
        " -",
        feature
    )


print("\nRemoved Features:")

for feature in removed_features:

    print(
        " -",
        feature
    )


# ============================================================
# 14. SAVE FEATURE SELECTION RESULT
# ============================================================

feature_status = []

for feature in X.columns:

    if feature in selected_features:

        status = "Selected"

    else:

        status = "Removed"

    feature_status.append({
        "Feature": feature,
        "Status": status
    })


feature_status_df = pd.DataFrame(
    feature_status
)


feature_status_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "selected_features.csv"
    ),
    index=False
)


# ============================================================
# 15. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("FEATURE SELECTION ANALYSIS COMPLETED")
print("=" * 70)

print("\nResults saved to:")

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