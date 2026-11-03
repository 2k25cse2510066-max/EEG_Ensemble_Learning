from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.calibration import CalibratedClassifierCV

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import (
    RandomForestClassifier,
    StackingClassifier
)

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)


# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "dataset" / "EEG_Extracted_Features.csv"
RESULTS_DIR = BASE_DIR / "results"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# LOAD FIVE-CLASS DATASET
# ==========================================

df = pd.read_csv(DATA_PATH)

print("Dataset Loaded Successfully")
print("Dataset Shape:", df.shape)

print("\nDataset Columns:")
print(df.columns.tolist())

print("\nClass Distribution:")
print(df["Label"].value_counts())


# ==========================================
# FEATURES AND TARGET
# ==========================================

X = df.drop("Label", axis=1)
y = df["Label"]


# ==========================================
# TRAIN-TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\n========== TRAIN-TEST SPLIT ==========")

print("Training Samples:", len(X_train))
print("Testing Samples:", len(X_test))

print("\nTraining Class Distribution:")
print(y_train.value_counts())

print("\nTesting Class Distribution:")
print(y_test.value_counts())


# ==========================================
# BASE MODEL 1: CALIBRATED SVM
# ==========================================

svm_base = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", SVC(
        kernel="rbf",
        C=1.0,
        gamma="scale",
        random_state=42
    ))
])

svm_model = CalibratedClassifierCV(
    estimator=svm_base,
    method="sigmoid",
    cv=5
)


# ==========================================
# BASE MODEL 2: RANDOM FOREST
# ==========================================

random_forest_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)


# ==========================================
# BASE MODEL 3: LOGISTIC REGRESSION
# ==========================================

logistic_model = Pipeline([
    ("scaler", StandardScaler()),
    ("logistic", LogisticRegression(
        max_iter=1000,
        random_state=42
    ))
])


# ==========================================
# STACKING CLASSIFIER
# ==========================================

estimators = [
    ("svm", svm_model),
    ("random_forest", random_forest_model),
    ("logistic_regression", logistic_model)
]

stacking_model = StackingClassifier(
    estimators=estimators,

    final_estimator=LogisticRegression(
        max_iter=1000,
        random_state=42
    ),

    cv=5,
    n_jobs=-1
)


# ==========================================
# TRAINING
# ==========================================

print("\n========== MODEL TRAINING ==========")
print("Training Stacking Classifier...")

stacking_model.fit(X_train, y_train)

print("Training Completed Successfully!")


# ==========================================
# PREDICTION
# ==========================================

y_pred = stacking_model.predict(X_test)

y_probability = stacking_model.predict_proba(X_test)


# ==========================================
# MULTICLASS METRICS
# ==========================================

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

roc_auc = roc_auc_score(
    y_test,
    y_probability,
    multi_class="ovr",
    average="weighted"
)


# ==========================================
# PRINT RESULTS
# ==========================================

print("\n========== STACKING CLASSIFIER RESULTS ==========")

print(f"Accuracy:  {accuracy * 100:.2f}%")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")
print(f"ROC-AUC:   {roc_auc:.4f}")


# ==========================================
# CLASSIFICATION REPORT
# ==========================================

print("\n========== CLASSIFICATION REPORT ==========")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# ==========================================
# CONFUSION MATRIX
# ==========================================

labels = list(stacking_model.classes_)

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
    "Stacking Classifier - 5-Class EEG Confusion Matrix",
    fontsize=17,
    pad=20
)

ax.set_xlabel(
    "Predicted Label",
    fontsize=13
)

ax.set_ylabel(
    "Actual Label",
    fontsize=13
)

ax.tick_params(
    axis="both",
    labelsize=10
)

plt.tight_layout()

confusion_matrix_path = (
    RESULTS_DIR / "stacking_5class_confusion_matrix.png"
)

plt.savefig(
    confusion_matrix_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nConfusion matrix saved successfully!")
print("Saved at:", confusion_matrix_path)


# ==========================================
# SAVE RESULTS
# ==========================================

results = pd.DataFrame({
    "Metric": [
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "ROC-AUC"
    ],

    "Value": [
        accuracy,
        precision,
        recall,
        f1,
        roc_auc
    ]
})

results_path = RESULTS_DIR / "stacking_5class_results.csv"

results.to_csv(
    results_path,
    index=False
)

print("\nResults saved successfully!")
print("Saved at:", results_path)