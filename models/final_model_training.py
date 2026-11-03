# ============================================================
# FINAL EXTRA TREES MODEL TRAINING
# EEG Ensemble Learning Project
# ============================================================

import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.preprocessing import LabelEncoder


# ------------------------------------------------------------
# 1. PROJECT PATHS
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "EEG_Engineered_Features.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

RESULTS_DIR = os.path.join(
    BASE_DIR,
    "results",
    "final_model"
)

os.makedirs(RESULTS_DIR, exist_ok=True)


# ------------------------------------------------------------
# 2. LOAD DATASET
# ------------------------------------------------------------

print("=" * 70)
print("FINAL EXTRA TREES MODEL TRAINING")
print("=" * 70)

df = pd.read_csv(DATA_PATH)

print("\nDataset shape:", df.shape)


# ------------------------------------------------------------
# 3. FEATURES AND LABEL
# ------------------------------------------------------------

X = df.drop("Label", axis=1)

label_encoder = LabelEncoder()

y = label_encoder.fit_transform(
    df["Label"]
)

feature_names = X.columns.tolist()

print("Number of features:", len(feature_names))
print("Number of samples:", len(X))

print("\nClasses:")

for i, class_name in enumerate(label_encoder.classes_):
    print(f"{i} -> {class_name}")


# ------------------------------------------------------------
# 4. DEFINE FINAL EXTRA TREES MODEL
# ------------------------------------------------------------

model = ExtraTreesClassifier(
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


# ------------------------------------------------------------
# 5. TRAIN ON FULL DATASET
# ------------------------------------------------------------

print("\nTraining final model on full dataset...")

model.fit(X, y)

print("Training completed successfully.")


# ------------------------------------------------------------
# 6. SAVE MODEL
# ------------------------------------------------------------

model_path = os.path.join(
    MODEL_DIR,
    "extra_trees_final.pkl"
)

with open(model_path, "wb") as file:
    pickle.dump(model, file)

print("\nModel saved:")
print(model_path)


# ------------------------------------------------------------
# 7. SAVE LABEL ENCODER
# ------------------------------------------------------------

encoder_path = os.path.join(
    MODEL_DIR,
    "label_encoder.pkl"
)

with open(encoder_path, "wb") as file:
    pickle.dump(label_encoder, file)

print("\nLabel encoder saved:")
print(encoder_path)


# ------------------------------------------------------------
# 8. SAVE FEATURE NAMES
# ------------------------------------------------------------

feature_path = os.path.join(
    MODEL_DIR,
    "feature_names.csv"
)

pd.DataFrame({
    "Feature": feature_names
}).to_csv(
    feature_path,
    index=False
)

print("\nFeature list saved:")
print(feature_path)


# ------------------------------------------------------------
# 9. FEATURE IMPORTANCE
# ------------------------------------------------------------

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": model.feature_importances_
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

importance_csv = os.path.join(
    RESULTS_DIR,
    "final_feature_importance.csv"
)

importance_df.to_csv(
    importance_csv,
    index=False
)

print("\nFeature importance saved:")
print(importance_csv)


# ------------------------------------------------------------
# 10. DISPLAY TOP 15 FEATURES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TOP 15 FEATURES")
print("=" * 70)

print(
    importance_df.head(15).to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 11. FEATURE IMPORTANCE PLOT
# ------------------------------------------------------------

top_features = importance_df.head(15)

plt.figure(figsize=(10, 7))

plt.barh(
    top_features["Feature"][::-1],
    top_features["Importance"][::-1]
)

plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Extra Trees - Top 15 EEG Feature Importance")

plt.tight_layout()

plot_path = os.path.join(
    RESULTS_DIR,
    "final_feature_importance.png"
)

plt.savefig(
    plot_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nFeature importance plot saved:")
print(plot_path)


# ------------------------------------------------------------
# 12. SAVE MODEL INFORMATION
# ------------------------------------------------------------

model_info = pd.DataFrame({
    "Parameter": [
        "Model",
        "Number of Trees",
        "Criterion",
        "Max Depth",
        "Min Samples Split",
        "Min Samples Leaf",
        "Max Features",
        "Class Weight",
        "Random State",
        "Training Samples",
        "Number of Features",
        "CV Accuracy",
        "Holdout Accuracy"
    ],
    "Value": [
        "Extra Trees Classifier",
        1000,
        "entropy",
        20,
        3,
        1,
        "sqrt",
        "balanced",
        42,
        len(X),
        len(feature_names),
        "87.80% +/- 5.40%",
        "89.00%"
    ]
})

info_path = os.path.join(
    RESULTS_DIR,
    "final_model_information.csv"
)

model_info.to_csv(
    info_path,
    index=False
)

print("\nModel information saved:")
print(info_path)


# ------------------------------------------------------------
# 13. FINAL SUMMARY
# ------------------------------------------------------------

print("\n")
print("=" * 70)
print("FINAL MODEL TRAINING COMPLETED")
print("=" * 70)

print("\nModel:")
print("Extra Trees Classifier")

print("\nValidation:")
print("10-Fold CV Accuracy: 87.80% +/- 5.40%")

print("\nHoldout:")
print("80/20 Accuracy: 89.00%")

print("\nModel file:")
print(model_path)

print("\nAll files generated successfully.")