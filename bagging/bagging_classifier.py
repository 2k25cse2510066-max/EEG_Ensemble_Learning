from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import (
    RandomForestClassifier,
    BaggingClassifier
)
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)


# =========================
# Project Paths
# =========================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_PATH = (
    PROJECT_ROOT
    / "dataset"
    / "EEG_Extracted_Features.csv"
)

RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# =========================
# Load Dataset
# =========================

df = pd.read_csv(DATASET_PATH)

print("Dataset Loaded Successfully")
print("Dataset Shape:", df.shape)


X = df.drop("Label", axis=1)
y = df["Label"]


# =========================
# Same Train-Test Split
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining Samples:", len(X_train))
print("Testing Samples:", len(X_test))


# =========================
# Random Forest Model
# =========================

random_forest = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)


# =========================
# Bagging Classifier Model
# =========================

base_tree = DecisionTreeClassifier(
    random_state=42
)

bagging_model = BaggingClassifier(
    estimator=base_tree,
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)


# =========================
# Train Models
# =========================

print("\nTraining Random Forest...")
random_forest.fit(X_train, y_train)
print("Random Forest Training Completed!")

print("\nTraining Bagging Classifier...")
bagging_model.fit(X_train, y_train)
print("Bagging Classifier Training Completed!")


# =========================
# Predictions
# =========================

rf_pred = random_forest.predict(X_test)
bagging_pred = bagging_model.predict(X_test)


# =========================
# Calculate Metrics
# =========================

rf_accuracy = accuracy_score(y_test, rf_pred)
rf_precision = precision_score(
    y_test,
    rf_pred,
    average="weighted",
    zero_division=0
)
rf_recall = recall_score(
    y_test,
    rf_pred,
    average="weighted",
    zero_division=0
)
rf_f1 = f1_score(
    y_test,
    rf_pred,
    average="weighted",
    zero_division=0
)


bagging_accuracy = accuracy_score(y_test, bagging_pred)
bagging_precision = precision_score(
    y_test,
    bagging_pred,
    average="weighted",
    zero_division=0
)
bagging_recall = recall_score(
    y_test,
    bagging_pred,
    average="weighted",
    zero_division=0
)
bagging_f1 = f1_score(
    y_test,
    bagging_pred,
    average="weighted",
    zero_division=0
)


# =========================
# Print Results
# =========================

print("\n========== RANDOM FOREST RESULTS ==========")

print(f"Accuracy:  {rf_accuracy * 100:.2f}%")
print(f"Precision: {rf_precision:.4f}")
print(f"Recall:    {rf_recall:.4f}")
print(f"F1-score:  {rf_f1:.4f}")


print("\n========== BAGGING CLASSIFIER RESULTS ==========")

print(f"Accuracy:  {bagging_accuracy * 100:.2f}%")
print(f"Precision: {bagging_precision:.4f}")
print(f"Recall:    {bagging_recall:.4f}")
print(f"F1-score:  {bagging_f1:.4f}")


# =========================
# Classification Reports
# =========================

print("\n========== RANDOM FOREST CLASSIFICATION REPORT ==========")
print(classification_report(y_test, rf_pred))

print("\n========== BAGGING CLASSIFIER CLASSIFICATION REPORT ==========")
print(classification_report(y_test, bagging_pred))


# =========================
# Comparison DataFrame
# =========================

comparison_df = pd.DataFrame({
    "Metric": [
        "Accuracy",
        "Precision",
        "Recall",
        "F1-score"
    ],
    "Random Forest": [
        rf_accuracy,
        rf_precision,
        rf_recall,
        rf_f1
    ],
    "Bagging Classifier": [
        bagging_accuracy,
        bagging_precision,
        bagging_recall,
        bagging_f1
    ]
})

print("\n========== MODEL COMPARISON ==========")
print(comparison_df.to_string(index=False))


# Save comparison results
comparison_df.to_csv(
    RESULTS_DIR / "random_forest_vs_bagging_comparison.csv",
    index=False
)


# =========================
# Plot Comparison Graph
# =========================

metrics = comparison_df["Metric"]
rf_scores = comparison_df["Random Forest"]
bagging_scores = comparison_df["Bagging Classifier"]

x = np.arange(len(metrics))
width = 0.35

plt.figure(figsize=(11, 7))

plt.bar(
    x - width / 2,
    rf_scores,
    width,
    label="Random Forest"
)

plt.bar(
    x + width / 2,
    bagging_scores,
    width,
    label="Bagging Classifier"
)


# Add values above bars
for i, value in enumerate(rf_scores):
    plt.text(
        i - width / 2,
        value + 0.01,
        f"{value:.3f}",
        ha="center",
        fontsize=10
    )

for i, value in enumerate(bagging_scores):
    plt.text(
        i + width / 2,
        value + 0.01,
        f"{value:.3f}",
        ha="center",
        fontsize=10
    )


plt.xlabel("Evaluation Metrics", fontsize=13)
plt.ylabel("Score", fontsize=13)

plt.title(
    "Random Forest vs Bagging Classifier",
    fontsize=16,
    fontweight="bold"
)

plt.xticks(x, metrics)
plt.ylim(0, 1.10)

plt.legend(fontsize=11)

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.6
)

plt.tight_layout()


# Save graph
output_path = RESULTS_DIR / "random_forest_vs_bagging.png"

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

print("\nComparison graph saved successfully at:")
print(output_path)

plt.show()