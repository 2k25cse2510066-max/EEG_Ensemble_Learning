import pandas as pd
import numpy as np

from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import (
    RandomForestClassifier,
    ExtraTreesClassifier,
    HistGradientBoostingClassifier
)
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier


# ============================================================
# LOAD DATA
# ============================================================

FILE = r"dataset\EEG_Engineered_Features.csv"

df = pd.read_csv(FILE)

from sklearn.preprocessing import LabelEncoder

X = df.drop("Label", axis=1)

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["Label"])


print("\n" + "=" * 75)
print("EEG MODEL COMPARISON - LEAKAGE-SAFE 10-FOLD CV")
print("=" * 75)

print("\nDataset shape:", df.shape)
print("Features:", X.shape[1])
print("Samples:", X.shape[0])


# ============================================================
# CROSS VALIDATION
# ============================================================

cv = StratifiedKFold(
    n_splits=10,
    shuffle=True,
    random_state=42
)


# ============================================================
# MODELS
# ============================================================

models = {

    "Random Forest": Pipeline([
        (
            "model",
            RandomForestClassifier(
                n_estimators=500,
                random_state=42,
                n_jobs=-1
            )
        )
    ]),

    "Extra Trees": Pipeline([
        (
            "model",
            ExtraTreesClassifier(
                n_estimators=500,
                random_state=42,
                n_jobs=-1
            )
        )
    ]),

    "XGBoost": Pipeline([
        (
            "model",
            XGBClassifier(
                n_estimators=100,
                max_depth=4,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                objective="multi:softprob",
                num_class=5,
                eval_metric="mlogloss",
                random_state=42,
                n_jobs=-1
            )
        )
    ]),

    "LightGBM": Pipeline([
        (
            "model",
            LGBMClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=-1,
                random_state=42,
                verbosity=-1,
                n_jobs=-1
            )
        )
    ]),

    "CatBoost": Pipeline([
        (
            "model",
            CatBoostClassifier(
                iterations=300,
                depth=6,
                learning_rate=0.05,
                verbose=False,
                random_seed=42
            )
        )
    ]),

    "SVM RBF": Pipeline([
        (
            "scaler",
            StandardScaler()
        ),
        (
            "model",
            SVC(
                kernel="rbf",
                C=1.0
            )
        )
    ]),

    "Logistic Regression": Pipeline([
        (
            "scaler",
            StandardScaler()
        ),
        (
            "model",
            LogisticRegression(
                max_iter=2000,
                random_state=42
            )
        )
    ]),

    "LDA": Pipeline([
        (
            "scaler",
            StandardScaler()
        ),
        (
            "model",
            LinearDiscriminantAnalysis()
        )
    ]),

    "QDA": Pipeline([
        (
            "scaler",
            StandardScaler()
        ),
        (
            "model",
            QuadraticDiscriminantAnalysis()
        )
    ]),

    "HistGradientBoosting": Pipeline([
        (
            "model",
            HistGradientBoostingClassifier(
                max_iter=200,
                learning_rate=0.1,
                random_state=42
            )
        )
    ])
}


# ============================================================
# RUN EXPERIMENT
# ============================================================

results = []

print("\nRunning 10-fold cross-validation...\n")

for name, model in models.items():

    print("-" * 75)
    print("Model:", name)

    scores = cross_val_score(
        model,
        X,
        y,
        cv=cv,
        scoring="accuracy",
        n_jobs=-1
    )

    mean_score = scores.mean() * 100
    std_score = scores.std() * 100

    print(
        f"Mean Accuracy: {mean_score:.2f}%"
    )

    print(
        f"Std Deviation: {std_score:.2f}%"
    )

    print("Fold Scores:")

    print(
        " ".join(
            f"{score * 100:.2f}%"
            for score in scores
        )
    )

    results.append({
        "Model": name,
        "Mean Accuracy (%)": round(mean_score, 2),
        "Std Deviation (%)": round(std_score, 2),
        "Minimum (%)": round(scores.min() * 100, 2),
        "Maximum (%)": round(scores.max() * 100, 2)
    })


# ============================================================
# RESULTS TABLE
# ============================================================

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="Mean Accuracy (%)",
    ascending=False
).reset_index(drop=True)


# ============================================================
# SAVE RESULTS
# ============================================================

OUTPUT_FILE = r"results\model_comparison_10fold.csv"

results_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# DISPLAY FINAL LEADERBOARD
# ============================================================

print("\n")
print("=" * 75)
print("FINAL MODEL LEADERBOARD")
print("=" * 75)

print(
    results_df.to_string(index=False)
)

print("\nResults saved to:")
print(OUTPUT_FILE)

print("\nExperiment completed.")