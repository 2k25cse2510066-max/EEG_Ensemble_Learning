from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


# Project root aur results folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "dataset" / "EEG_Extracted_Features.csv"
RESULTS_DIR = PROJECT_ROOT / "results"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# Dataset load
df = pd.read_csv(DATASET_PATH)

print("Dataset Loaded Successfully")
print("Dataset Shape:", df.shape)


# Features aur target
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


# Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

print("\nTraining Random Forest...")
model.fit(X_train, y_train)
print("Training Completed!")


# Prediction
y_pred = model.predict(X_test)


# Classification report
report = classification_report(
    y_test,
    y_pred,
    output_dict=True
)


# Sirf five class rows select karna
class_names = model.classes_

precision = [report[class_name]["precision"] for class_name in class_names]
recall = [report[class_name]["recall"] for class_name in class_names]
f1_score = [report[class_name]["f1-score"] for class_name in class_names]


# Graph settings
x = np.arange(len(class_names))
width = 0.25

plt.figure(figsize=(14, 7))

plt.bar(
    x - width,
    precision,
    width,
    label="Precision"
)

plt.bar(
    x,
    recall,
    width,
    label="Recall"
)

plt.bar(
    x + width,
    f1_score,
    width,
    label="F1-score"
)


# Labels and title
plt.xlabel("EEG Classes", fontsize=13)
plt.ylabel("Score", fontsize=13)

plt.title(
    "Random Forest: Precision, Recall, and F1-score",
    fontsize=16,
    fontweight="bold"
)

plt.xticks(
    x,
    class_names,
    rotation=20,
    ha="right"
)

plt.ylim(0, 1.05)
plt.yticks(np.arange(0, 1.1, 0.1))

plt.legend(fontsize=11)
plt.grid(axis="y", linestyle="--", alpha=0.6)

plt.tight_layout()


# Graph save
output_path = RESULTS_DIR / "random_forest_precision_recall_f1.png"

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

print("\nGraph saved successfully at:")
print(output_path)

plt.show()