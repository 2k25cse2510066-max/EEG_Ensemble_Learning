import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    roc_auc_score
)

from xgboost import XGBClassifier


# ============================================================
# 1. LOAD ENGINEERED DATASET
# ============================================================

data = pd.read_csv(
    r"C:\Users\Vaishnav kant\Desktop\EEG_Ensemble_Learning\dataset\EEG_Engineered_Features.csv"
)

X = data.drop("Label", axis=1)
y = data["Label"]


# ============================================================
# 2. ENCODE LABELS
# ============================================================

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

print("Classes:")
print(label_encoder.classes_)


# ============================================================
# 3. TRAIN-TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.20,
    random_state=42,
    stratify=y_encoded
)


# ============================================================
# 4. RANDOM FOREST
# ============================================================

rf = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)


# ============================================================
# 5. XGBOOST
# ============================================================

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


# ============================================================
# 6. SVM
# ============================================================

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
# 7. STACKING MODEL
# ============================================================

stacking_model = StackingClassifier(
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
# 8. TRAIN
# ============================================================

print("\nTraining Final Engineered Stacking Model...")

stacking_model.fit(X_train, y_train)


# ============================================================
# 9. PREDICTION
# ============================================================

y_pred = stacking_model.predict(X_test)
y_prob = stacking_model.predict_proba(X_test)


# ============================================================
# 10. METRICS
# ============================================================

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
    y_prob,
    multi_class="ovr",
    average="weighted"
)


# ============================================================
# 11. PRINT RESULTS
# ============================================================

print("\n==========================================")
print("FINAL ENGINEERED STACKING RESULTS")
print("==========================================")

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC-AUC   : {roc_auc:.4f}")


print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_,
        zero_division=0
    )
)


# ============================================================
# 12. CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)


# ============================================================
# 13. SAVE CONFUSION MATRIX
# ============================================================

plt.figure(figsize=(9, 7))

plt.imshow(cm, interpolation="nearest")
plt.title("Final Engineered Stacking Confusion Matrix")
plt.colorbar()

plt.xticks(
    range(len(label_encoder.classes_)),
    label_encoder.classes_,
    rotation=45,
    ha="right"
)

plt.yticks(
    range(len(label_encoder.classes_)),
    label_encoder.classes_
)

for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(
            j,
            i,
            cm[i, j],
            ha="center",
            va="center"
        )

plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.tight_layout()

plt.savefig(
    r"C:\Users\Vaishnav kant\Desktop\EEG_Ensemble_Learning\results\final_engineered_stacking_confusion_matrix.png",
    dpi=300
)

plt.show()


# ============================================================
# 14. SAVE RESULTS
# ============================================================

results = pd.DataFrame({
    "Metric": [
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "ROC-AUC"
    ],
    "Score": [
        accuracy,
        precision,
        recall,
        f1,
        roc_auc
    ]
})

results.to_csv(
    r"C:\Users\Vaishnav kant\Desktop\EEG_Ensemble_Learning\results\final_engineered_stacking_results.csv",
    index=False
)

print("\nResults saved successfully.")