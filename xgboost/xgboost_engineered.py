import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

from xgboost import XGBClassifier


# ============================================================
# 1. PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "dataset" / "EEG_Extracted_Features.csv"
RESULTS_DIR = BASE_DIR / "results"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. LOAD DATASET
# ============================================================

df = pd.read_csv(DATA_PATH)

print("Dataset Shape:", df.shape)
print("\nClass Distribution:")
print(df["Label"].value_counts())


# ============================================================
# 3. FEATURES AND TARGET
# ============================================================

X = df.drop("Label", axis=1)
y = df["Label"]


# ============================================================
# 4. ENCODE LABELS
# ============================================================

label_encoder = LabelEncoder()

y_encoded = label_encoder.fit_transform(y)

print("\nClasses:")
for i, label in enumerate(label_encoder.classes_):
    print(i, "=", label)


# ============================================================
# 5. TRAIN-TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.20,
    random_state=42,
    stratify=y_encoded
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ============================================================
# 6. XGBOOST MODEL
# ============================================================

model = XGBClassifier(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="multi:softprob",
    num_class=len(label_encoder.classes_),
    eval_metric="mlogloss",
    random_state=42
)


# ============================================================
# 7. TRAIN MODEL
# ============================================================

print("\nTraining XGBoost...")

model.fit(X_train, y_train)

print("Training completed!")


# ============================================================
# 8. PREDICTION
# ============================================================

y_pred = model.predict(X_test)


# ============================================================
# 9. EVALUATION
# ============================================================

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    average="weighted"
)

recall = recall_score(
    y_test,
    y_pred,
    average="weighted"
)

f1 = f1_score(
    y_test,
    y_pred,
    average="weighted"
)


print("\n======================================")
print("        XGBOOST RESULTS")
print("======================================")

print(f"Accuracy  : {accuracy * 100:.2f}%")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1-Score  : {f1:.4f}")


# ============================================================
# 10. CLASSIFICATION REPORT
# ============================================================

print("\n========== CLASSIFICATION REPORT ==========")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_
    )
)


# ============================================================
# 11. CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_test,
    y_pred
)

print("\n========== CONFUSION MATRIX ==========")
print(cm)


fig, ax = plt.subplots(figsize=(11, 8))

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=label_encoder.classes_
)

disp.plot(
    ax=ax,
    values_format="d",
    cmap="Blues",
    colorbar=True,
    xticks_rotation=25
)

ax.set_title(
    "XGBoost - 5-Class EEG Confusion Matrix",
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

plt.tight_layout()


# ============================================================
# 12. SAVE CONFUSION MATRIX
# ============================================================

output_path = RESULTS_DIR / "xgboost_confusion_matrix.png"

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nConfusion matrix saved successfully!")
print("Saved at:", output_path)


# ============================================================
# 13. SAVE PERFORMANCE RESULTS
# ============================================================

results = pd.DataFrame({
    "Model": ["XGBoost"],
    "Accuracy": [accuracy],
    "Precision": [precision],
    "Recall": [recall],
    "F1_Score": [f1]
})

results_path = RESULTS_DIR / "xgboost_results.csv"

results.to_csv(
    results_path,
    index=False
)

print("Results saved at:", results_path)