# ============================================================
# EEG MODEL PREDICTION
# Load trained Extra Trees model and predict EEG class
# ============================================================

import os
import pickle
import pandas as pd


# ------------------------------------------------------------
# 1. PATHS
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "extra_trees_final.pkl"
)

ENCODER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "label_encoder.pkl"
)

FEATURE_PATH = os.path.join(
    BASE_DIR,
    "models",
    "feature_names.csv"
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "EEG_Engineered_Features.csv"
)


# ------------------------------------------------------------
# 2. LOAD MODEL
# ------------------------------------------------------------

print("=" * 70)
print("EEG MODEL PREDICTION")
print("=" * 70)

print("\nLoading trained model...")

with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

print("Model loaded successfully.")


# ------------------------------------------------------------
# 3. LOAD LABEL ENCODER
# ------------------------------------------------------------

with open(ENCODER_PATH, "rb") as file:
    label_encoder = pickle.load(file)

print("Label encoder loaded successfully.")


# ------------------------------------------------------------
# 4. LOAD FEATURE LIST
# ------------------------------------------------------------

feature_df = pd.read_csv(FEATURE_PATH)

feature_names = feature_df["Feature"].tolist()

print("Feature list loaded successfully.")
print("Number of expected features:", len(feature_names))


# ------------------------------------------------------------
# 5. LOAD TEST DATA
# ------------------------------------------------------------
#
# IMPORTANT:
# This uses the engineered dataset only to demonstrate that
# the saved model can successfully make predictions.
#
# The model was already trained on the full dataset, so this
# is NOT an independent accuracy evaluation.
# ------------------------------------------------------------

df = pd.read_csv(DATA_PATH)

X = df.drop("Label", axis=1)

# Make sure feature order is exactly the same
X = X[feature_names]


# ------------------------------------------------------------
# 6. SELECT ONE SAMPLE
# ------------------------------------------------------------

sample_index = 0

sample = X.iloc[[sample_index]]


# ------------------------------------------------------------
# 7. PREDICT
# ------------------------------------------------------------

prediction_encoded = model.predict(sample)

prediction_label = label_encoder.inverse_transform(
    prediction_encoded
)[0]


# ------------------------------------------------------------
# 8. PREDICTION PROBABILITIES
# ------------------------------------------------------------

probabilities = model.predict_proba(sample)[0]

probability_df = pd.DataFrame({
    "Class": label_encoder.classes_,
    "Probability": probabilities
})

probability_df = probability_df.sort_values(
    by="Probability",
    ascending=False
)


# ------------------------------------------------------------
# 9. DISPLAY RESULT
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("PREDICTION RESULT")
print("=" * 70)

print("\nSample index:", sample_index)

print("\nPredicted class:")
print(prediction_label)

print("\nClass probabilities:")

for _, row in probability_df.iterrows():

    print(
        f"{row['Class']:<30} "
        f"{row['Probability'] * 100:.2f}%"
    )


# ------------------------------------------------------------
# 10. DISPLAY ACTUAL LABEL
# ------------------------------------------------------------

actual_label = df.iloc[sample_index]["Label"]

print("\nActual dataset label:")
print(actual_label)


# ------------------------------------------------------------
# 11. COMPARISON
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("PREDICTION CHECK")
print("=" * 70)

if prediction_label == actual_label:

    print("\nPrediction matches the dataset label.")

else:

    print("\nPrediction does NOT match the dataset label.")


print("\n")
print("=" * 70)
print("PREDICTION COMPLETED")
print("=" * 70)