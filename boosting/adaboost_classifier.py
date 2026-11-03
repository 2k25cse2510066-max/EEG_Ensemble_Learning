from pathlib import Path

import matplotlib.pyplot as plt

from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay
)
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier
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
# AdaBoost Model
# =========================

base_tree = DecisionTreeClassifier(
    max_depth=1,
    random_state=42
)

model = AdaBoostClassifier(
    estimator=base_tree,
    n_estimators=100,
    learning_rate=1.0,
    random_state=42
)


# =========================
# Training
# =========================

print("\nTraining AdaBoost Classifier...")
model.fit(X_train, y_train)
print("AdaBoost Training Completed!")


# =========================
# Prediction
# =========================

y_pred = model.predict(X_test)
# ==========================================
# ADABOOST CONFUSION MATRIX
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

labels = list(model.classes_)

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=labels
)

print("\n========== CONFUSION MATRIX ==========")
print(cm)

fig, ax = plt.subplots(figsize=(11, 8))

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=labels
)

disp.plot(
    ax=ax,
    values_format="d",
    cmap="Blues",
    colorbar=True,
    xticks_rotation=25
)

ax.set_title(
    "AdaBoost - 5-Class EEG Confusion Matrix",
    fontsize=17,
    pad=20
)

ax.set_xlabel("Predicted Label", fontsize=13)
ax.set_ylabel("Actual Label", fontsize=13)

plt.tight_layout()

output_path = RESULTS_DIR / "adaboost_confusion_matrix.png"

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nConfusion matrix saved successfully!")
print("Saved at:", output_path)

# =========================
# Evaluation Metrics
# =========================

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)


# =========================
# Print Results
# =========================

print("\n========== ADABOOST RESULTS ==========")

print(f"Accuracy:  {accuracy * 100:.2f}%")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-score:  {f1:.4f}")


print("\n========== ADABOOST CLASSIFICATION REPORT ==========")
print(classification_report(y_test, y_pred))


# =========================
# Save Results
# =========================

results_df = pd.DataFrame({
    "Metric": [
        "Accuracy",
        "Precision",
        "Recall",
        "F1-score"
    ],
    "AdaBoost": [
        accuracy,
        precision,
        recall,
        f1
    ]
})

results_df.to_csv(
    RESULTS_DIR / "adaboost_results.csv",
    index=False
)


# =========================
# Plot Metrics
# =========================

metrics = results_df["Metric"]
scores = results_df["AdaBoost"]

x = np.arange(len(metrics))

plt.figure(figsize=(10, 6))

plt.bar(x, scores)

for i, score in enumerate(scores):
    plt.text(
        i,
        score + 0.01,
        f"{score:.3f}",
        ha="center",
        fontsize=11
    )

plt.xlabel("Evaluation Metrics", fontsize=13)
plt.ylabel("Score", fontsize=13)

plt.title(
    "AdaBoost Classifier Performance",
    fontsize=16,
    fontweight="bold"
)

plt.xticks(x, metrics)
plt.ylim(0, 1.10)

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.6
)

plt.tight_layout()


# =========================
# Save Graph
# =========================

output_path = RESULTS_DIR / "adaboost_performance.png"

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

print("\nGraph saved successfully at:")
print(output_path)

plt.show()