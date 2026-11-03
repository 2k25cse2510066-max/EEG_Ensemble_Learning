from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import (
    train_test_split,
    GridSearchCV,
    StratifiedKFold
)

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    make_scorer
)


# ==============================
# PROJECT PATHS
# ==============================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "dataset" / "EEG_Binary_Classification.csv"
RESULTS_DIR = BASE_DIR / "results"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ==============================
# LOAD DATASET
# ==============================

df = pd.read_csv(DATA_PATH)

print("Dataset Loaded Successfully")
print("Dataset Shape:", df.shape)

X = df.drop("Label", axis=1)
y = df["Label"]


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
# SVM PIPELINE
# ==============================

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", SVC(
        probability=False,
        random_state=42
    ))
])


# ==============================
# HYPERPARAMETER GRID
# ==============================

param_grid = {
    "svm__C": [0.1, 1, 10, 100],
    "svm__gamma": ["scale", 0.001, 0.01, 0.1, 1],
    "svm__kernel": ["rbf", "linear", "poly"]
}


# ==============================
# SCORING
# ==============================

f1_scorer = make_scorer(
    f1_score,
    pos_label="Epileptic"
)

cv_strategy = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


# ==============================
# GRID SEARCH
# ==============================

grid_search = GridSearchCV(
    estimator=pipeline,
    param_grid=param_grid,
    scoring=f1_scorer,
    cv=cv_strategy,
    n_jobs=-1,
    verbose=1
)

print("\nStarting Grid Search...")

grid_search.fit(X_train, y_train)

print("\nGrid Search Completed!")


# ==============================
# BEST PARAMETERS
# ==============================

print("\n========== BEST PARAMETERS ==========")

print("Best Parameters:")
print(grid_search.best_params_)

print("\nBest Cross-Validation F1 Score:")
print(f"{grid_search.best_score_:.4f}")


# ==============================
# TEST PREDICTION
# ==============================

best_model = grid_search.best_estimator_

y_pred = best_model.predict(X_test)

y_score = best_model.decision_function(X_test)


# ==============================
# PERFORMANCE METRICS
# ==============================

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    pos_label="Epileptic"
)

recall = recall_score(
    y_test,
    y_pred,
    pos_label="Epileptic"
)

f1 = f1_score(
    y_test,
    y_pred,
    pos_label="Epileptic"
)

roc_auc = roc_auc_score(
    y_test,
    y_score
)


print("\n========== OPTIMIZED SVM RESULTS ==========")

print(f"Accuracy:  {accuracy * 100:.2f}%")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")
print(f"ROC-AUC:   {roc_auc:.4f}")


# ==============================
# CLASSIFICATION REPORT
# ==============================

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred
    )
)


# ==============================
# CONFUSION MATRIX
# ==============================

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=["Epileptic", "Non_Epileptic"]
)

print("\nConfusion Matrix:")
print(cm)

fig, ax = plt.subplots(figsize=(8, 6))

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Epileptic", "Non-Epileptic"]
)

disp.plot(
    ax=ax,
    values_format="d",
    cmap="Blues",
    colorbar=True
)

ax.set_title(
    "Optimized SVM - Binary EEG Classification",
    fontsize=16,
    pad=15
)

ax.set_xlabel("Predicted Label")
ax.set_ylabel("Actual Label")

plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "optimized_svm_confusion_matrix.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


print("\nConfusion matrix saved successfully!")