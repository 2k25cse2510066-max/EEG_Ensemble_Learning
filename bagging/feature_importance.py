from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "dataset" / "EEG_Extracted_Features.csv"
RESULTS_DIR = PROJECT_ROOT / "results"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# Dataset load
df = pd.read_csv(DATASET_PATH)

print("Dataset Loaded Successfully")
print("Dataset Shape:", df.shape)


# Features and target
X = df.drop("Label", axis=1)
y = df["Label"]


# Same train-test split as Random Forest
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# Train Random Forest
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

print("\nTraining Random Forest...")
model.fit(X_train, y_train)
print("Training Completed!")


# Feature importance
importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

# Highest importance first
importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)


print("\n========== FEATURE IMPORTANCE ==========")
print(importance_df.to_string(index=False))


# Plot
plt.figure(figsize=(12, 7))

plt.barh(
    importance_df["Feature"],
    importance_df["Importance"]
)

plt.xlabel("Importance Score", fontsize=13)
plt.ylabel("EEG Features", fontsize=13)

plt.title(
    "Random Forest Feature Importance",
    fontsize=16,
    fontweight="bold"
)

# Most important feature at the top
plt.gca().invert_yaxis()

plt.grid(
    axis="x",
    linestyle="--",
    alpha=0.6
)

plt.tight_layout()


# Save graph
output_path = RESULTS_DIR / "random_forest_feature_importance.png"

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

print("\nGraph saved successfully at:")
print(output_path)

plt.show()