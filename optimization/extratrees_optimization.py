import pandas as pd
import numpy as np

from sklearn.model_selection import (
    StratifiedKFold,
    RandomizedSearchCV,
    train_test_split
)

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# =========================================================
# 1. LOAD DATA
# =========================================================

df = pd.read_csv(r"dataset\EEG_Engineered_Features.csv")

X = df.drop("Label", axis=1)
y = LabelEncoder().fit_transform(df["Label"])

# =========================================================
# 2. FIXED TEST SET
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    stratify=y,
    random_state=42
)

# =========================================================
# 3. EXTRA TREES
# =========================================================

model = ExtraTreesClassifier(
    random_state=42,
    n_jobs=-1
)

# =========================================================
# 4. PARAMETER SEARCH
# =========================================================

param_grid = {
    "n_estimators": [300, 500, 700, 1000],
    "max_depth": [None, 10, 15, 20, 30, 40],
    "min_samples_split": [2, 3, 5, 8],
    "min_samples_leaf": [1, 2, 3, 4],
    "max_features": ["sqrt", "log2", None],
    "class_weight": [None, "balanced", "balanced_subsample"],
    "criterion": ["gini", "entropy", "log_loss"]
}

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

search = RandomizedSearchCV(
    estimator=model,
    param_distributions=param_grid,
    n_iter=50,
    scoring="accuracy",
    cv=cv,
    random_state=42,
    n_jobs=-1,
    verbose=1
)

print("\nStarting Extra Trees optimization...\n")

search.fit(X_train, y_train)

# =========================================================
# 5. BEST PARAMETERS
# =========================================================

print("\nBEST PARAMETERS:")
print(search.best_params_)

print("\nBEST CV ACCURACY:")
print(f"{search.best_score_ * 100:.2f}%")

# =========================================================
# 6. TEST SET EVALUATION
# =========================================================

best_model = search.best_estimator_

y_pred = best_model.predict(X_test)

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

print("\nTEST RESULTS")
print("=" * 50)

print(f"Accuracy  : {accuracy * 100:.2f}%")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")

print("\nCLASSIFICATION REPORT:")
print(
    classification_report(
        y_test,
        y_pred
    )
)

print("\nCONFUSION MATRIX:")
print(
    confusion_matrix(
        y_test,
        y_pred
    )
)

# =========================================================
# 7. SAVE RESULTS
# =========================================================

results = pd.DataFrame({
    "Metric": [
        "Best CV Accuracy",
        "Test Accuracy",
        "Precision",
        "Recall",
        "F1"
    ],
    "Value": [
        search.best_score_,
        accuracy,
        precision,
        recall,
        f1
    ]
})

results.to_csv(
    r"results\extratrees_optimization_results.csv",
    index=False
)

print("\nSaved:")
print(r"results\extratrees_optimization_results.csv")