from pathlib import Path

import pandas as pd

from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


# =========================
# 1. Load Dataset
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "EEG_Extracted_Features.csv"

df = pd.read_csv(DATA_PATH)

X = df.drop("Label", axis=1)
y = df["Label"]


# =========================
# 2. Define 5-Fold CV
# =========================

skf = StratifiedKFold(
    n_splits=15,
    shuffle=True,
    random_state=42
)


# =========================
# 3. Define Models
# =========================

random_forest = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

adaboost = AdaBoostClassifier(
    n_estimators=50,
    learning_rate=1.0,
    random_state=42
)

svm = make_pipeline(
    StandardScaler(),
    SVC(
        probability=True,
        kernel="rbf",
        random_state=42
    )
)

stacking = StackingClassifier(
    estimators=[
        ("random_forest", random_forest),
        ("adaboost", adaboost),
        ("svm", svm)
    ],
    final_estimator=LogisticRegression(
        max_iter=1000
    ),
    cv=5
)


models = {
    "Random Forest": random_forest,
    "AdaBoost": adaboost,
    "Stacking": stacking
}


# =========================
# 4. Run Cross-Validation
# =========================

print("\n========== 5-FOLD STRATIFIED CROSS-VALIDATION ==========\n")

results = {}

for model_name, model in models.items():

    scores = cross_val_score(
        model,
        X,
        y,
        cv=skf,
        scoring="accuracy",
        n_jobs=-1
    )

    average_score = scores.mean()
    standard_deviation = scores.std()

    results[model_name] = {
        "Fold 1": scores[0],
        "Fold 2": scores[1],
        "Fold 3": scores[2],
        "Fold 4": scores[3],
        "Fold 5": scores[4],
        "Average Accuracy": average_score,
        "Standard Deviation": standard_deviation
    }

    print(f"\n{model_name}")
    print("-" * 40)

    for i, score in enumerate(scores, start=1):
        print(f"Fold {i} Accuracy: {score * 100:.2f}%")

    print(f"Average Accuracy: {average_score * 100:.2f}%")
    print(f"Standard Deviation: {standard_deviation * 100:.2f}%")


# =========================
# 5. Save Results
# =========================

results_df = pd.DataFrame(results).T

RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

output_path = RESULTS_DIR / "cross_validation_results.csv"

results_df.to_csv(output_path)

print("\n==============================================")
print("Cross-validation results saved successfully!")
print("Saved at:", output_path)
print("==============================================")