import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, StratifiedKFold, RandomizedSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from xgboost import XGBClassifier


# =========================
# 1. Load Dataset
# =========================

df = pd.read_csv("../dataset/EEG_Extracted_Features.csv")

X = df.drop("Label", axis=1)
y = df["Label"]


# =========================
# 2. Encode Labels
# =========================

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)


# =========================
# 3. Train-Test Split
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# =========================
# 4. Base XGBoost Model
# =========================

xgb = XGBClassifier(
    objective="multi:softprob",
    num_class=5,
    eval_metric="mlogloss",
    random_state=42,
    n_jobs=-1
)


# =========================
# 5. Hyperparameter Search Space
# =========================

param_grid = {
    "n_estimators": [100, 200, 300, 400, 500],
    "max_depth": [2, 3, 4, 5, 6, 8],
    "learning_rate": [0.01, 0.03, 0.05, 0.1, 0.15],
    "min_child_weight": [1, 2, 3, 5],
    "subsample": [0.7, 0.8, 0.9, 1.0],
    "colsample_bytree": [0.7, 0.8, 0.9, 1.0],
    "gamma": [0, 0.1, 0.2, 0.5, 1],
    "reg_alpha": [0, 0.01, 0.1, 0.5],
    "reg_lambda": [0.5, 1, 1.5, 2, 5]
}


# =========================
# 6. Cross Validation
# =========================

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


# =========================
# 7. Randomized Search
# =========================

random_search = RandomizedSearchCV(
    estimator=xgb,
    param_distributions=param_grid,
    n_iter=30,
    scoring="accuracy",
    cv=cv,
    verbose=2,
    random_state=42,
    n_jobs=-1
)


print("\nStarting XGBoost Hyperparameter Optimization...\n")

random_search.fit(X_train, y_train)


# =========================
# 8. Best Parameters
# =========================

print("\n==============================")
print("BEST PARAMETERS")
print("==============================")

print(random_search.best_params_)

print("\nBest CV Accuracy:",
      random_search.best_score_ * 100)


# =========================
# 9. Evaluate Best Model
# =========================

best_model = random_search.best_estimator_

y_pred = best_model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n==============================")
print("TEST RESULTS")
print("==============================")

print("Accuracy:", accuracy * 100, "%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_
    )
)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))