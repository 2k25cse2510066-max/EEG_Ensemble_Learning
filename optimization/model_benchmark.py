import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import (
    LinearDiscriminantAnalysis,
    QuadraticDiscriminantAnalysis
)
from sklearn.ensemble import (
    ExtraTreesClassifier,
    HistGradientBoostingClassifier,
    RandomForestClassifier
)

# Load engineered dataset
df = pd.read_csv(r"dataset\EEG_Engineered_Features.csv")

X = df.drop("Label", axis=1)
y = LabelEncoder().fit_transform(df["Label"])

# Same leakage-safe CV used earlier
cv = StratifiedKFold(
    n_splits=10,
    shuffle=True,
    random_state=42
)

models = {
    "SVM_RBF": Pipeline([
        ("scaler", StandardScaler()),
        ("model", SVC(C=1, kernel="rbf"))
    ]),

    "SVM_Linear": Pipeline([
        ("scaler", StandardScaler()),
        ("model", SVC(C=1, kernel="linear"))
    ]),

    "Logistic": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=3000))
    ]),

    "LDA": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LinearDiscriminantAnalysis())
    ]),

    "QDA": Pipeline([
        ("scaler", StandardScaler()),
        ("model", QuadraticDiscriminantAnalysis(reg_param=0.1))
    ]),

    "ExtraTrees": ExtraTreesClassifier(
        n_estimators=500,
        random_state=42,
        n_jobs=-1
    ),

    "HistGB": HistGradientBoostingClassifier(
        max_iter=300,
        learning_rate=0.05,
        max_leaf_nodes=15,
        l2_regularization=1,
        random_state=42
    ),

    "RF": RandomForestClassifier(
        n_estimators=500,
        random_state=42,
        n_jobs=-1
    )
}

print("\n10-FOLD LEAKAGE-SAFE MODEL BENCHMARK")
print("=" * 55)

results = []

for name, model in models.items():

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

    results.append({
        "Model": name,
        "Mean Accuracy": mean_score,
        "Std": std_score
    })

    print(
        f"{name:15s}: "
        f"{mean_score:.2f}% ± {std_score:.2f}%"
    )

print("=" * 55)

result_df = pd.DataFrame(results)
result_df = result_df.sort_values(
    "Mean Accuracy",
    ascending=False
)

print("\nRANKED RESULTS:")
print(result_df.to_string(index=False))

result_df.to_csv(
    r"results\model_benchmark_results.csv",
    index=False
)

print("\nSaved:")
print(r"results\model_benchmark_results.csv")
