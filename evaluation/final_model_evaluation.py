# ============================================================
# FINAL MODEL EVALUATION
# LightGBM + Extra Trees
# 80/20 Stratified Train-Test Split
# ============================================================

import os
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)
from sklearn.ensemble import ExtraTreesClassifier
from lightgbm import LGBMClassifier


# ------------------------------------------------------------
# 1. PATHS
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "EEG_Engineered_Features.csv"
)

RESULTS_DIR = os.path.join(
    BASE_DIR,
    "results",
    "final_evaluation"
)

os.makedirs(RESULTS_DIR, exist_ok=True)


# ------------------------------------------------------------
# 2. LOAD DATASET
# ------------------------------------------------------------

print("=" * 70)
print("FINAL MODEL EVALUATION")
print("LightGBM + Extra Trees")
print("=" * 70)

df = pd.read_csv(DATA_PATH)

print("\nDataset shape:", df.shape)
print("Number of samples:", len(df))
print("Number of features:", df.shape[1] - 1)


# ------------------------------------------------------------
# 3. SEPARATE FEATURES AND LABEL
# ------------------------------------------------------------

X = df.drop("Label", axis=1)

# Encode string class labels into integers
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["Label"])

class_names = label_encoder.classes_

print("\nClasses:")
for i, name in enumerate(class_names):
    print(i, "->", name)


# ------------------------------------------------------------
# 4. 80/20 STRATIFIED TRAIN-TEST SPLIT
# ------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    stratify=y,
    random_state=42
)

print("\nTrain samples:", len(X_train))
print("Test samples:", len(X_test))

print("\nTrain class distribution:")
print(pd.Series(y_train).value_counts().sort_index())

print("\nTest class distribution:")
print(pd.Series(y_test).value_counts().sort_index())


# ------------------------------------------------------------
# 5. DEFINE MODELS
# ------------------------------------------------------------

models = {

    "LightGBM": LGBMClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=-1,
        num_leaves=31,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        verbosity=-1
    ),

    "Extra Trees": ExtraTreesClassifier(
        n_estimators=1000,
        criterion="entropy",
        max_depth=20,
        min_samples_split=3,
        min_samples_leaf=1,
        max_features="sqrt",
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
}


# ------------------------------------------------------------
# 6. STORAGE FOR RESULTS
# ------------------------------------------------------------

comparison_results = []


# ------------------------------------------------------------
# 7. TRAIN AND EVALUATE EACH MODEL
# ------------------------------------------------------------

for model_name, model in models.items():

    print("\n")
    print("=" * 70)
    print(model_name)
    print("=" * 70)

    # Train
    print("\nTraining model...")

    model.fit(X_train, y_train)

    # Prediction
    y_pred = model.predict(X_test)

    # Metrics
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

    # --------------------------------------------------------
    # PRINT MAIN METRICS
    # --------------------------------------------------------

    print("\nPerformance:")
    print("-" * 40)

    print(f"Accuracy  : {accuracy * 100:.2f}%")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1-Score  : {f1:.4f}")


    # --------------------------------------------------------
    # CONFUSION MATRIX
    # --------------------------------------------------------

    cm = confusion_matrix(
        y_test,
        y_pred,
        labels=np.arange(len(class_names))
    )

    print("\nConfusion Matrix:")
    print(cm)


    # --------------------------------------------------------
    # CLASSIFICATION REPORT
    # --------------------------------------------------------

    report = classification_report(
        y_test,
        y_pred,
        labels=np.arange(len(class_names)),
        target_names=class_names,
        zero_division=0
    )

    print("\nClassification Report:")
    print(report)


    # --------------------------------------------------------
    # SAVE CONFUSION MATRIX
    # --------------------------------------------------------

    cm_df = pd.DataFrame(
        cm,
        index=class_names,
        columns=class_names
    )

    cm_path = os.path.join(
        RESULTS_DIR,
        model_name.lower().replace(" ", "_") + "_confusion_matrix.csv"
    )

    cm_df.to_csv(cm_path)


    # --------------------------------------------------------
    # SAVE CLASSIFICATION REPORT
    # --------------------------------------------------------

    report_dict = classification_report(
        y_test,
        y_pred,
        labels=np.arange(len(class_names)),
        target_names=class_names,
        output_dict=True,
        zero_division=0
    )

    report_df = pd.DataFrame(report_dict).transpose()

    report_path = os.path.join(
        RESULTS_DIR,
        model_name.lower().replace(" ", "_") + "_classification_report.csv"
    )

    report_df.to_csv(report_path)


    # --------------------------------------------------------
    # SAVE MODEL RESULTS
    # --------------------------------------------------------

    comparison_results.append({
        "Model": model_name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1_Score": f1
    })


# ------------------------------------------------------------
# 8. MODEL COMPARISON
# ------------------------------------------------------------

comparison_df = pd.DataFrame(comparison_results)

print("\n")
print("=" * 70)
print("FINAL MODEL COMPARISON")
print("=" * 70)

print("\n")
print(comparison_df.to_string(index=False))


# ------------------------------------------------------------
# 9. SAVE COMPARISON CSV
# ------------------------------------------------------------

comparison_path = os.path.join(
    RESULTS_DIR,
    "final_model_comparison.csv"
)

comparison_df.to_csv(
    comparison_path,
    index=False
)


# ------------------------------------------------------------
# 10. FINAL SUMMARY
# ------------------------------------------------------------

print("\n")
print("=" * 70)
print("FILES SAVED")
print("=" * 70)

print("\nResults folder:")
print(RESULTS_DIR)

print("\nGenerated files:")

for file_name in os.listdir(RESULTS_DIR):
    print("-", file_name)


print("\n")
print("=" * 70)
print("EVALUATION COMPLETED SUCCESSFULLY")
print("=" * 70)