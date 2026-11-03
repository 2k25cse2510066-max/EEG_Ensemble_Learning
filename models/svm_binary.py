import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_auc_score,
    RocCurveDisplay
)

# ==============================
# PROJECT PATHS
# ==============================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_PATH = (
    PROJECT_ROOT
    / "dataset"
    / "EEG_Binary_Classification.csv"
)

RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# ==============================
# LOAD DATASET
# ==============================

df = pd.read_csv(DATASET_PATH)

print("Dataset Loaded Successfully")
print("Dataset Shape:", df.shape)

X = df.drop("Binary_Label", axis=1)
y = df["Binary_Label"]

# ==============================
# TRAIN-TEST SPLIT
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining Samples:", len(X_train))
print("Testing Samples:", len(X_test))

# ==============================
# SVM MODEL
# ==============================

svm_model = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", SVC(
        kernel="rbf",
        C=1.0,
        gamma="scale",
        probability=True,
        random_state=42
    ))
])

print("\nTraining SVM...")
svm_model.fit(X_train, y_train)
print("SVM Training Completed!")

# ==============================
# PREDICTION
# ==============================

y_pred = svm_model.predict(X_test)

# Probability of the positive class
positive_class = "Epileptic"
positive_index = list(svm_model.classes_).index(positive_class)

y_prob = svm_model.predict_proba(X_test)[:, positive_index]

# ==============================
# PERFORMANCE METRICS
# ==============================

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    pos_label=positive_class,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    pos_label=positive_class,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    pos_label=positive_class,
    zero_division=0
)

auc = roc_auc_score(
    (y_test == positive_class).astype(int),
    y_prob
)

print("\n========== SVM RESULTS ==========")
print(f"Accuracy:  {accuracy * 100:.2f}%")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-score:  {f1:.4f}")
print(f"ROC-AUC:   {auc:.4f}")

print("\n========== SVM CLASSIFICATION REPORT ==========")
print(classification_report(y_test, y_pred))

# ==============================
# CONFUSION MATRIX
# ==============================

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=svm_model.classes_
)

print("\n========== CONFUSION MATRIX ==========")
print(cm)

fig, ax = plt.subplots(figsize=(8, 6))

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=svm_model.classes_
)

disp.plot(
    ax=ax,
    values_format="d",
    cmap="Blues",
    colorbar=True
)

ax.set_title(
    "SVM - Binary EEG Classification Confusion Matrix",
    fontsize=16,
    pad=15
)

ax.set_xlabel("Predicted Label")
ax.set_ylabel("Actual Label")

plt.tight_layout()

confusion_path = RESULTS_DIR / "svm_binary_confusion_matrix.png"

plt.savefig(
    confusion_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nConfusion Matrix saved successfully at:")
print(confusion_path)

# ==============================
# ROC CURVE
# ==============================

fig, ax = plt.subplots(figsize=(8, 6))

RocCurveDisplay.from_predictions(
    (y_test == positive_class).astype(int),
    y_prob,
    name=f"SVM (AUC = {auc:.4f})",
    ax=ax
)

ax.plot(
    [0, 1],
    [0, 1],
    linestyle="--",
    label="Random Classifier"
)

ax.set_title(
    "SVM - Binary EEG ROC Curve",
    fontsize=16,
    pad=15
)

ax.set_xlabel("False Positive Rate")
ax.set_ylabel("True Positive Rate")

ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()

roc_path = RESULTS_DIR / "svm_binary_roc_auc.png"

plt.savefig(
    roc_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nROC Curve saved successfully at:")
print(roc_path)

print("\nSVM Binary Classification Completed Successfully!")