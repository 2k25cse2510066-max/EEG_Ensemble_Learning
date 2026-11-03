import pandas as pd
import numpy as np

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectFromModel


# ============================================================
# LOAD DATA
# ============================================================

FILE = r"dataset\EEG_Advanced_Features.csv"

df = pd.read_csv(FILE)

X = df.drop("Label", axis=1)
y = df["Label"]


print("\n" + "=" * 70)
print("ADVANCED FEATURES - LEAKAGE-SAFE 10-FOLD CV")
print("=" * 70)

print("\nDataset shape:", df.shape)
print("Number of features:", X.shape[1])
print("Number of samples:", X.shape[0])


# ============================================================
# FEATURE SELECTION
# IMPORTANT:
# Selector is INSIDE pipeline, so it is fitted separately
# inside every CV training fold.
# ============================================================

selector = SelectFromModel(
    ExtraTreesClassifier(
        n_estimators=500,
        random_state=42,
        n_jobs=-1
    ),
    threshold="median"
)


# ============================================================
# FINAL CLASSIFIER
# ============================================================

classifier = ExtraTreesClassifier(
    n_estimators=500,
    random_state=42,
    n_jobs=-1
)


# ============================================================
# PIPELINE
# ============================================================

pipeline = Pipeline([
    ("feature_selection", selector),
    ("classifier", classifier)
])


# ============================================================
# STRATIFIED 10-FOLD CV
# ============================================================

cv = StratifiedKFold(
    n_splits=10,
    shuffle=True,
    random_state=42
)


scores = cross_val_score(
    pipeline,
    X,
    y,
    cv=cv,
    scoring="accuracy",
    n_jobs=-1
)


# ============================================================
# RESULTS
# ============================================================

print("\nFOLD ACCURACIES:")

for i, score in enumerate(scores, start=1):
    print(
        f"Fold {i:2d}: {score * 100:.2f}%"
    )


mean_accuracy = scores.mean() * 100
std_accuracy = scores.std() * 100
min_accuracy = scores.min() * 100
max_accuracy = scores.max() * 100


print("\n" + "=" * 70)
print("FINAL RESULTS")
print("=" * 70)

print(
    f"\nMean Accuracy : {mean_accuracy:.2f}%"
)

print(
    f"Std Deviation : {std_accuracy:.2f}%"
)

print(
    f"Minimum       : {min_accuracy:.2f}%"
)

print(
    f"Maximum       : {max_accuracy:.2f}%"
)


# ============================================================
# COMPARISON
# ============================================================

previous_best = 88.00

print("\n" + "=" * 70)
print("COMPARISON")
print("=" * 70)

print(
    f"\nPrevious best independent CV : {previous_best:.2f}%"
)

print(
    f"Advanced-feature CV          : {mean_accuracy:.2f}%"
)

difference = mean_accuracy - previous_best

print(
    f"Difference                   : {difference:+.2f}%"
)


if difference > 0:
    print(
        "\nResult: Advanced features improved CV accuracy."
    )

elif difference < 0:
    print(
        "\nResult: Advanced features did NOT improve CV accuracy."
    )

else:
    print(
        "\nResult: Performance remained the same."
    )


print("\nExperiment completed.")