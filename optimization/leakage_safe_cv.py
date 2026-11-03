import pandas as pd
import numpy as np

from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier


# ============================================================
# 1. LOAD ENGINEERED DATA
# ============================================================

data = pd.read_csv(
    r"C:\Users\Vaishnav kant\Desktop\EEG_Ensemble_Learning\dataset\EEG_Engineered_Features.csv"
)

X = data.drop("Label", axis=1)
y = data["Label"]


# ============================================================
# 2. ENCODE LABELS
# ============================================================

encoder = LabelEncoder()
y = encoder.fit_transform(y)


# ============================================================
# 3. FEATURE SELECTION
# ============================================================

feature_selector = SelectFromModel(
    RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    ),
    threshold="median"
)


# ============================================================
# 4. BASE MODELS
# ============================================================

rf = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)


xgb = XGBClassifier(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="multi:softprob",
    num_class=5,
    eval_metric="mlogloss",
    random_state=42
)


svm = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", SVC(
        kernel="rbf",
        C=1.0,
        probability=True,
        random_state=42
    ))
])


# ============================================================
# 5. STACKING
# ============================================================

stacking = StackingClassifier(
    estimators=[
        ("rf", rf),
        ("xgb", xgb),
        ("svm", svm)
    ],
    final_estimator=LogisticRegression(
        max_iter=2000,
        random_state=42
    ),
    cv=5,
    stack_method="predict_proba",
    n_jobs=-1
)


# ============================================================
# 6. COMPLETE PIPELINE
# ============================================================

model = Pipeline([
    ("feature_selection", feature_selector),
    ("stacking", stacking)
])


# ============================================================
# 7. 10-FOLD STRATIFIED CROSS VALIDATION
# ============================================================

cv = StratifiedKFold(
    n_splits=10,
    shuffle=True,
    random_state=42
)

print("\n==========================================")
print("LEAKAGE-SAFE 10-FOLD CROSS VALIDATION")
print("==========================================")

scores = cross_val_score(
    model,
    X,
    y,
    cv=cv,
    scoring="accuracy",
    n_jobs=1
)


# ============================================================
# 8. DISPLAY FOLD RESULTS
# ============================================================

print("\nFold Accuracies:")

for i, score in enumerate(scores, start=1):
    print(f"Fold {i:2d}: {score * 100:.2f}%")


# ============================================================
# 9. FINAL STATISTICS
# ============================================================

mean_accuracy = np.mean(scores)
std_accuracy = np.std(scores)

print("\n==========================================")
print("FINAL CROSS-VALIDATION RESULT")
print("==========================================")

print(f"Mean Accuracy : {mean_accuracy * 100:.2f}%")
print(f"Std Deviation : {std_accuracy * 100:.2f}%")

print("\nIndividual Scores:")
print(scores)