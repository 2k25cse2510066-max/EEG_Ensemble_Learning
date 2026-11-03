from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc, roc_auc_score


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "dataset" / "EEG_Extracted_Features.csv"
RESULTS_DIR = PROJECT_ROOT / "results"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# Dataset load
df = pd.read_csv(DATASET_PATH)

print("Dataset Loaded Successfully")
print("Dataset Shape:", df.shape)


# Features and target
X = df.drop("Label", axis=1)
y = df["Label"]


# Same train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# Train Random Forest
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

print("\nTraining Random Forest...")
model.fit(X_train, y_train)
print("Training Completed!")


# Probability prediction
y_score = model.predict_proba(X_test)

# Convert actual labels into binary format
y_test_binary = label_binarize(
    y_test,
    classes=model.classes_
)

class_names = model.classes_


# Calculate ROC-AUC for each class
roc_auc_scores = {}

for i, class_name in enumerate(class_names):
    fpr, tpr, _ = roc_curve(
        y_test_binary[:, i],
        y_score[:, i]
    )

    roc_auc_scores[class_name] = auc(fpr, tpr)


# Print AUC scores
print("\n========== ROC-AUC SCORES ==========")

for class_name, score in roc_auc_scores.items():
    print(f"{class_name}: {score:.4f}")

macro_auc = roc_auc_score(
    y_test_binary,
    y_score,
    multi_class="ovr",
    average="macro"
)

weighted_auc = roc_auc_score(
    y_test_binary,
    y_score,
    multi_class="ovr",
    average="weighted"
)

print(f"\nMacro-average AUC: {macro_auc:.4f}")
print(f"Weighted-average AUC: {weighted_auc:.4f}")


# Plot ROC curves
plt.figure(figsize=(12, 8))

for i, class_name in enumerate(class_names):
    fpr, tpr, _ = roc_curve(
        y_test_binary[:, i],
        y_score[:, i]
    )

    roc_auc_value = auc(fpr, tpr)

    plt.plot(
        fpr,
        tpr,
        linewidth=2,
        label=f"{class_name} (AUC = {roc_auc_value:.3f})"
    )


# Random classifier baseline
plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--",
    linewidth=1.5,
    label="Random Classifier (AUC = 0.500)"
)


plt.xlabel("False Positive Rate", fontsize=13)
plt.ylabel("True Positive Rate", fontsize=13)

plt.title(
    "Random Forest - Multiclass ROC Curve",
    fontsize=16,
    fontweight="bold"
)

plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])

plt.grid(
    linestyle="--",
    alpha=0.6
)

plt.legend(
    loc="lower right",
    fontsize=9
)

plt.tight_layout()


# Save graph
output_path = RESULTS_DIR / "random_forest_roc_auc.png"

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

print("\nROC Curve saved successfully at:")
print(output_path)

plt.show()