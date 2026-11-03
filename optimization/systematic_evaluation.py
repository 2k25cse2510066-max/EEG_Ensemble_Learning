# ============================================================
# SYSTEMATIC EEG MODEL EVALUATION
# Feature Selection + Stacking + Proper 10-Fold Validation
# ============================================================

import os
import warnings
import numpy as np
import pandas as pd

from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, mutual_info_classif, SelectFromModel
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier, StackingClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score

warnings.filterwarnings("ignore")


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
    "systematic_evaluation"
)

os.makedirs(RESULTS_DIR, exist_ok=True)


# ------------------------------------------------------------
# 2. LOAD DATA
# ------------------------------------------------------------

print("=" * 75)
print("SYSTEMATIC EEG MODEL EVALUATION")
print("=" * 75)

df = pd.read_csv(DATA_PATH)

X = df.drop("Label", axis=1)

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["Label"])

feature_names = X.columns.tolist()

print("\nDataset shape:", df.shape)
print("Samples:", len(X))
print("Features:", len(feature_names))

print("\nClasses:")
for i, name in enumerate(label_encoder.classes_):
    print(f"{i} -> {name}")


# ------------------------------------------------------------
# 3. CROSS-VALIDATION
# ------------------------------------------------------------

cv = StratifiedKFold(
    n_splits=10,
    shuffle=True,
    random_state=42
)


# ------------------------------------------------------------
# 4. COMMON MODELS
# ------------------------------------------------------------

extra_trees = ExtraTreesClassifier(
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


rf_selector = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)


xgb_model = None

try:
    from xgboost import XGBClassifier

    xgb_model = XGBClassifier(
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

except ImportError:
    print("\nXGBoost not available.")


# Calibrated SVM so stacking can use probabilities
svm_model = Pipeline([
    (
        "scaler",
        StandardScaler()
    ),
    (
        "svc",
        CalibratedClassifierCV(
            SVC(
                C=1.0,
                kernel="rbf",
                gamma="scale"
            ),
            cv=3,
            method="sigmoid"
        )
    )
])


# ------------------------------------------------------------
# 5. SCORING
# ------------------------------------------------------------

scoring = {
    "accuracy": make_scorer(accuracy_score),
    "precision": make_scorer(
        precision_score,
        average="weighted",
        zero_division=0
    ),
    "recall": make_scorer(
        recall_score,
        average="weighted",
        zero_division=0
    ),
    "f1": make_scorer(
        f1_score,
        average="weighted",
        zero_division=0
    )
}


# ------------------------------------------------------------
# 6. DEFINE EXPERIMENTS
# ------------------------------------------------------------

experiments = {}


# ------------------------------------------------------------
# EXPERIMENT 1
# BASELINE EXTRA TREES
# ------------------------------------------------------------

experiments["Extra Trees Baseline"] = extra_trees


# ------------------------------------------------------------
# EXPERIMENT 2
# MUTUAL INFORMATION + EXTRA TREES
# ------------------------------------------------------------

experiments["MI Feature Selection + Extra Trees"] = Pipeline([
    (
        "feature_selection",
        SelectKBest(
            score_func=mutual_info_classif,
            k=8
        )
    ),
    (
        "model",
        extra_trees
    )
])


# ------------------------------------------------------------
# EXPERIMENT 3
# MODEL-BASED FEATURE SELECTION + EXTRA TREES
# ------------------------------------------------------------

experiments["RF Feature Selection + Extra Trees"] = Pipeline([
    (
        "feature_selection",
        SelectFromModel(
            estimator=rf_selector,
            threshold="median"
        )
    ),
    (
        "model",
        extra_trees
    )
])


# ------------------------------------------------------------
# EXPERIMENT 4
# STACKING WITHOUT FEATURE SELECTION
# ------------------------------------------------------------

stack_estimators = [
    (
        "extra_trees",
        ExtraTreesClassifier(
            n_estimators=500,
            criterion="entropy",
            max_depth=20,
            min_samples_split=3,
            min_samples_leaf=1,
            max_features="sqrt",
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        )
    ),
    (
        "xgboost",
        xgb_model
    ) if xgb_model is not None else (
        "extra_trees_2",
        ExtraTreesClassifier(
            n_estimators=500,
            random_state=43,
            n_jobs=-1
        )
    ),
    (
        "svm",
        svm_model
    )
]

stacking_model = StackingClassifier(
    estimators=stack_estimators,
    final_estimator=LogisticRegression(
        max_iter=2000,
        random_state=42
    ),
    cv=5,
    stack_method="predict_proba",
    n_jobs=-1
)

experiments["Stacking"] = stacking_model


# ------------------------------------------------------------
# EXPERIMENT 5
# FEATURE SELECTION + STACKING
# ------------------------------------------------------------

feature_selected_stacking = Pipeline([
    (
        "feature_selection",
        SelectFromModel(
            estimator=RandomForestClassifier(
                n_estimators=300,
                random_state=42,
                n_jobs=-1
            ),
            threshold="median"
        )
    ),
    (
        "stacking",
        stacking_model
    )
])

experiments["RF Feature Selection + Stacking"] = feature_selected_stacking


# ------------------------------------------------------------
# 7. RUN EXPERIMENTS
# ------------------------------------------------------------

all_results = []

print("\n")
print("=" * 75)
print("RUNNING 10-FOLD STRATIFIED CROSS-VALIDATION")
print("=" * 75)

for name, model in experiments.items():

    print("\n" + "-" * 75)
    print(name)
    print("-" * 75)

    try:

        results = cross_validate(
            model,
            X,
            y,
            cv=cv,
            scoring=scoring,
            n_jobs=1,
            return_train_score=False
        )

        accuracy_scores = results["test_accuracy"]
        precision_scores = results["test_precision"]
        recall_scores = results["test_recall"]
        f1_scores = results["test_f1"]

        print("\nAccuracy folds:")
        print(
            " ".join(
                f"{score * 100:.2f}%"
                for score in accuracy_scores
            )
        )

        print(
            f"\nAccuracy : "
            f"{accuracy_scores.mean() * 100:.2f}% "
            f"+/- {accuracy_scores.std() * 100:.2f}%"
        )

        print(
            f"Precision: "
            f"{precision_scores.mean():.4f}"
        )

        print(
            f"Recall   : "
            f"{recall_scores.mean():.4f}"
        )

        print(
            f"F1-Score : "
            f"{f1_scores.mean():.4f}"
        )

        all_results.append({
            "Model": name,
            "Accuracy_Mean": accuracy_scores.mean(),
            "Accuracy_STD": accuracy_scores.std(),
            "Precision_Mean": precision_scores.mean(),
            "Recall_Mean": recall_scores.mean(),
            "F1_Mean": f1_scores.mean()
        })

    except Exception as e:

        print("\nERROR:")
        print(str(e))


# ------------------------------------------------------------
# 8. SAVE MODEL COMPARISON
# ------------------------------------------------------------

results_df = pd.DataFrame(all_results)

results_df = results_df.sort_values(
    by="Accuracy_Mean",
    ascending=False
)

comparison_path = os.path.join(
    RESULTS_DIR,
    "systematic_model_comparison.csv"
)

results_df.to_csv(
    comparison_path,
    index=False
)


# ------------------------------------------------------------
# 9. PRINT FINAL TABLE
# ------------------------------------------------------------

print("\n")
print("=" * 75)
print("FINAL SYSTEMATIC COMPARISON")
print("=" * 75)

print(
    results_df.to_string(index=False)
)


# ------------------------------------------------------------
# 10. FEATURE IMPORTANCE
# ------------------------------------------------------------

print("\n")
print("=" * 75)
print("EXTRA TREES FEATURE IMPORTANCE")
print("=" * 75)

# Train only for descriptive explainability.
# This is NOT used to claim CV performance.

explain_model = ExtraTreesClassifier(
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

explain_model.fit(X, y)

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": explain_model.feature_importances_
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

importance_path = os.path.join(
    RESULTS_DIR,
    "extra_trees_feature_importance.csv"
)

importance_df.to_csv(
    importance_path,
    index=False
)

print("\nTop 15 features:")

print(
    importance_df.head(15).to_string(index=False)
)


# ------------------------------------------------------------
# 11. SAVE TOP FEATURES
# ------------------------------------------------------------

top_features_path = os.path.join(
    RESULTS_DIR,
    "top_features.csv"
)

importance_df.head(15).to_csv(
    top_features_path,
    index=False
)


# ------------------------------------------------------------
# 12. FINAL MESSAGE
# ------------------------------------------------------------

print("\n")
print("=" * 75)
print("SYSTEMATIC EVALUATION COMPLETED")
print("=" * 75)

print("\nResults saved in:")
print(RESULTS_DIR)

print("\nFiles:")

for filename in os.listdir(RESULTS_DIR):
    print("-", filename)

print("\n")
print("IMPORTANT:")
print("Cross-validation results are the primary generalization estimate.")
print("Feature importance is descriptive explainability only.")