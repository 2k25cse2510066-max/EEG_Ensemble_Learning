import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline

from sklearn.ensemble import (
    RandomForestClassifier,
    ExtraTreesClassifier,
    StackingClassifier
)

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    roc_auc_score
)


# =========================================================
# 1. LOAD ENGINEERED DATASET
# =========================================================

df = pd.read_csv(
    r"dataset\EEG_Engineered_Features.csv"
)

X = df.drop("Label", axis=1)

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["Label"])


# =========================================================
# 2. TRAIN / TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    stratify=y,
    random_state=42
)


# =========================================================
# 3. RANDOM FOREST
# =========================================================

rf = RandomForestClassifier(
    n_estimators=500,
    random_state=42,
    n_jobs=-1
)


# =========================================================
# 4. EXTRA TREES
# =========================================================

extra = ExtraTreesClassifier(
    n_estimators=1000,
    max_depth=20,
    min_samples_split=3,
    min_samples_leaf=1,
    max_features="sqrt",
    criterion="entropy",
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)


# =========================================================
# 5. XGBOOST
# =========================================================

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


# =========================================================
# 6. SVM
# =========================================================

svm = Pipeline([
    (
        "scaler",
        StandardScaler()
    ),
    (
        "model",
        SVC(
            C=1,
            kernel="rbf",
            probability=True
        )
    )
])


# =========================================================
# 7. BASE ESTIMATORS
# =========================================================

estimators = [
    ("rf", rf),
    ("extra", extra),
    ("xgb", xgb),
    ("svm", svm)
]


# =========================================================
# 8. META MODEL
# =========================================================

meta_model = LogisticRegression(
    max_iter=3000
)


# =========================================================
# 9. STACKING CLASSIFIER
# =========================================================

stacking = StackingClassifier(
    estimators=estimators,
    final_estimator=meta_model,
    cv=5,
    stack_method="predict_proba",
    n_jobs=-1
)


# =========================================================
# 10. TRAIN
# =========================================================

print("\nTraining 4-model stacking...\n")

stacking.fit(
    X_train,
    y_train
)


# =========================================================
# 11. PREDICTION
# =========================================================

y_pred = stacking.predict(
    X_test
)

y_prob = stacking.predict_proba(
    X_test
)


# =========================================================
# 12. METRICS
# =========================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

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

roc_auc = roc_auc_score(
    y_test,
    y_prob,
    multi_class="ovr",
    average="weighted"
)


# =========================================================
# 13. DISPLAY RESULTS
# =========================================================

print("=" * 60)
print("4-MODEL STACKING RESULTS")
print("=" * 60)

print(
    f"Accuracy  : {accuracy * 100:.2f}%"
)

print(
    f"Precision : {precision:.4f}"
)

print(
    f"Recall    : {recall:.4f}"
)

print(
    f"F1 Score  : {f1:.4f}"
)

print(
    f"ROC-AUC   : {roc_auc:.4f}"
)


# =========================================================
# 14. CLASSIFICATION REPORT
# =========================================================

print("\nCLASSIFICATION REPORT:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_
    )
)


# =========================================================
# 15. CONFUSION MATRIX
# =========================================================

print("\nCONFUSION MATRIX:")

cm = confusion_matrix(
    y_test,
    y_pred
)

print(cm)


# =========================================================
# 16. SAVE RESULTS
# =========================================================

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


results.to_csv(
    r"results\four_model_stacking_results.csv",
    index=False
)


# =========================================================
# 17. SAVE CONFUSION MATRIX
# =========================================================

cm_df = pd.DataFrame(
    cm,
    index=label_encoder.classes_,
    columns=label_encoder.classes_
)

cm_df.to_csv(
    r"results\four_model_stacking_confusion_matrix.csv"
)


print("\nSaved:")
print(
    r"results\four_model_stacking_results.csv"
)

print(
    r"results\four_model_stacking_confusion_matrix.csv"
)
