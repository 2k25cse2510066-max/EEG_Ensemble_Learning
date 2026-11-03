from pathlib import Path
import pandas as pd


# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = BASE_DIR / "dataset" / "EEG_Extracted_Features.csv"
OUTPUT_PATH = BASE_DIR / "dataset" / "EEG_Engineered_Features.csv"


# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(INPUT_PATH)

print("Original Dataset Shape:", df.shape)

print("\nOriginal Features:")
print(df.columns.tolist())


# ==========================================
# COPY DATA
# ==========================================

engineered_df = df.copy()


# ==========================================
# POWER RATIO FEATURES
# ==========================================

epsilon = 1e-10

engineered_df["delta_ratio"] = (
    engineered_df["delta_power"] /
    (engineered_df["total_power"] + epsilon)
)

engineered_df["theta_ratio"] = (
    engineered_df["theta_power"] /
    (engineered_df["total_power"] + epsilon)
)

engineered_df["alpha_ratio"] = (
    engineered_df["alpha_power"] /
    (engineered_df["total_power"] + epsilon)
)

engineered_df["beta_ratio"] = (
    engineered_df["beta_power"] /
    (engineered_df["total_power"] + epsilon)
)

engineered_df["gamma_ratio"] = (
    engineered_df["gamma_power"] /
    (engineered_df["total_power"] + epsilon)
)


# ==========================================
# BAND POWER RELATIONSHIPS
# ==========================================

engineered_df["theta_alpha_ratio"] = (
    engineered_df["theta_power"] /
    (engineered_df["alpha_power"] + epsilon)
)

engineered_df["delta_alpha_ratio"] = (
    engineered_df["delta_power"] /
    (engineered_df["alpha_power"] + epsilon)
)

engineered_df["delta_beta_ratio"] = (
    engineered_df["delta_power"] /
    (engineered_df["beta_power"] + epsilon)
)

engineered_df["theta_beta_ratio"] = (
    engineered_df["theta_power"] /
    (engineered_df["beta_power"] + epsilon)
)


# ==========================================
# COMBINED BAND FEATURES
# ==========================================

engineered_df["delta_theta_power"] = (
    engineered_df["delta_power"] +
    engineered_df["theta_power"]
)

engineered_df["alpha_beta_power"] = (
    engineered_df["alpha_power"] +
    engineered_df["beta_power"]
)


# ==========================================
# BAND DIFFERENCE FEATURES
# ==========================================

engineered_df["delta_alpha_difference"] = (
    engineered_df["delta_power"] -
    engineered_df["alpha_power"]
)

engineered_df["theta_alpha_difference"] = (
    engineered_df["theta_power"] -
    engineered_df["alpha_power"]
)

engineered_df["beta_gamma_difference"] = (
    engineered_df["beta_power"] -
    engineered_df["gamma_power"]
)


# ==========================================
# SAVE ENGINEERED DATASET
# ==========================================

engineered_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\n========== FEATURE ENGINEERING COMPLETE ==========")

print("Original Features:", df.shape[1])
print("Engineered Features:", engineered_df.shape[1])

print("\nNew Features:")

new_features = [
    column
    for column in engineered_df.columns
    if column not in df.columns
]

for feature in new_features:
    print("-", feature)


print("\nNew Dataset Shape:", engineered_df.shape)

print("\nSaved Successfully!")
print("File:", OUTPUT_PATH)