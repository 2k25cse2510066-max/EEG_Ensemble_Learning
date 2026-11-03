from pathlib import Path

import pandas as pd

from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    RandomizedSearchCV
)

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ============================================================
# 1. PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR /
    "dataset" /
    "EEG_Engineered_Features.csv"
)


# ============================================================
# 2. LOAD DATASET
# ============================================================

df = pd.read_csv(DATA_PATH)

print("Dataset Shape:", df.shape)


# ============================================================
# 3. FEATURES AND TARGET
# ============================================================

X = df.drop("Label", axis=1)
y = df["Label"]


# ============================================================
# 4. TRAIN-TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining Samples:", len(X_train))
print("Testing Samples:", len(X_test))


# ============================================================
# 5. RANDOM FOREST
# ============================================================

rf = RandomForestClassifier(
    random_state=42,
    n_jobs=-1
)


# ============================================================
# 6. HYPERPARAMETER SEARCH SPACE
# ============================================================

param_distributions = {

    "n_estimators": [
        100, 150, 200, 250, 300,
        400, 500, 600, 700
    ],

    "max_depth": [
        None, 5, 8, 10, 12,
        15, 20, 25, 30, 40
    ],

    "min_samples_split": [
        2, 3, 4, 5, 6, 8, 10
    ],

    "min_samples_leaf": [
        1, 2, 3, 4
    ],

    "max_features": [
        "sqrt",
        "log2",
        None
    ],

    "bootstrap": [
        True,
        False
    ],

    "class_weight": [
        None,
        "balanced"
    ]
}


# ============================================================
# 7. STRATIFIED CROSS VALIDATION
# ============================================================

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


# ============================================================
# 8. RANDOMIZED SEARCH
# ============================================================

search = RandomizedSearchCV(
    estimator=rf,
    param_distributions=param_distributions,
    n_iter=40,
    scoring="accuracy",
    cv=cv,
    verbose=2,
    random_state=42,
    n_jobs=-1
)


# ============================================================
# 9. TRAIN SEARCH
# ============================================================

print("\n==========================================")
print("STARTING ENGINEERED RF OPTIMIZATION")
print("==========================================")

search.fit(X_train, y_train)


# ============================================================
# 10. BEST PARAMETERS
# ============================================================

print("\n==========================================")
print("BEST PARAMETERS")
print("==========================================")

print(search.best_params_)

print(
    "\nBest CV Accuracy:",
    f"{search.best_score_ * 100:.2f}%"
)


# ============================================================
# 11. BEST MODEL
# ============================================================

best_rf = search.best_estimator_


# ============================================================
# 12. TEST SET PREDICTION
# ============================================================

y_pred = best_rf.predict(X_test)


# ============================================================
# 13. TEST ACCURACY
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)


print("\n==========================================")
print("ENGINEERED RF TEST RESULTS")
print("==========================================")

print(
    f"Test Accuracy: {accuracy * 100:.2f}%"
)


# ============================================================
# 14. CLASSIFICATION REPORT
# ============================================================

print("\n========== CLASSIFICATION REPORT ==========")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# ============================================================
# 15. CONFUSION MATRIX
# ============================================================

print("\n========== CONFUSION MATRIX ==========")

cm = confusion_matrix(
    y_test,
    y_pred
)

print(cm)