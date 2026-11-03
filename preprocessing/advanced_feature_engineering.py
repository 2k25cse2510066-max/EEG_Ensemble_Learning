import os
import pandas as pd
import numpy as np


# ============================================================
# ADVANCED EEG FEATURE ENGINEERING
# ============================================================

INPUT_FILE = r"dataset\EEG_Extracted_Features.csv"
OUTPUT_FILE = r"dataset\EEG_Advanced_Features.csv"

EPSILON = 1e-10


# ============================================================
# LOAD DATA
# ============================================================

print("\n" + "=" * 70)
print("ADVANCED EEG FEATURE ENGINEERING")
print("=" * 70)

df = pd.read_csv(INPUT_FILE)

print(f"\nOriginal dataset shape: {df.shape}")


# ============================================================
# COPY DATA
# ============================================================

engineered = df.copy()


# ============================================================
# BAND POWER FEATURES
# ============================================================

delta = engineered["delta_power"]
theta = engineered["theta_power"]
alpha = engineered["alpha_power"]
beta = engineered["beta_power"]
gamma = engineered["gamma_power"]

total = engineered["total_power"]


# ============================================================
# 1. RELATIVE BAND POWERS
# ============================================================

engineered["relative_delta_power"] = (
    delta / (total + EPSILON)
)

engineered["relative_theta_power"] = (
    theta / (total + EPSILON)
)

engineered["relative_alpha_power"] = (
    alpha / (total + EPSILON)
)

engineered["relative_beta_power"] = (
    beta / (total + EPSILON)
)

engineered["relative_gamma_power"] = (
    gamma / (total + EPSILON)
)


# ============================================================
# 2. BAND POWER RATIOS
# ============================================================

engineered["theta_alpha_ratio"] = (
    theta / (alpha + EPSILON)
)

engineered["delta_alpha_ratio"] = (
    delta / (alpha + EPSILON)
)

engineered["delta_beta_ratio"] = (
    delta / (beta + EPSILON)
)

engineered["theta_beta_ratio"] = (
    theta / (beta + EPSILON)
)

engineered["alpha_beta_ratio"] = (
    alpha / (beta + EPSILON)
)

engineered["beta_gamma_ratio"] = (
    beta / (gamma + EPSILON)
)

engineered["delta_theta_ratio"] = (
    delta / (theta + EPSILON)
)

engineered["alpha_gamma_ratio"] = (
    alpha / (gamma + EPSILON)
)

engineered["theta_gamma_ratio"] = (
    theta / (gamma + EPSILON)
)


# ============================================================
# 3. BAND POWER DIFFERENCES
# ============================================================

engineered["delta_theta_difference"] = (
    delta - theta
)

engineered["theta_alpha_difference"] = (
    theta - alpha
)

engineered["alpha_beta_difference"] = (
    alpha - beta
)

engineered["beta_gamma_difference"] = (
    beta - gamma
)

engineered["delta_alpha_difference"] = (
    delta - alpha
)


# ============================================================
# 4. BAND POWER SUMS
# ============================================================

engineered["low_frequency_power"] = (
    delta + theta
)

engineered["high_frequency_power"] = (
    beta + gamma
)

engineered["alpha_beta_power"] = (
    alpha + beta
)

engineered["delta_theta_power"] = (
    delta + theta
)


# ============================================================
# 5. FREQUENCY-BALANCE FEATURES
# ============================================================

engineered["low_high_ratio"] = (
    (delta + theta + EPSILON)
    /
    (beta + gamma + EPSILON)
)

engineered["theta_alpha_beta_ratio"] = (
    (theta + EPSILON)
    /
    (alpha + beta + EPSILON)
)

engineered["delta_theta_alpha_ratio"] = (
    (delta + theta + EPSILON)
    /
    (alpha + EPSILON)
)


# ============================================================
# 6. NORMALIZED STATISTICAL FEATURES
# ============================================================

engineered["range_to_std_ratio"] = (
    engineered["range"]
    /
    (engineered["std"] + EPSILON)
)

engineered["rms_to_std_ratio"] = (
    engineered["rms"]
    /
    (engineered["std"] + EPSILON)
)

engineered["variance_to_rms_ratio"] = (
    engineered["variance"]
    /
    (engineered["rms"] + EPSILON)
)


# ============================================================
# 7. ENERGY DISTRIBUTION FEATURES
# ============================================================

engineered["delta_fraction"] = (
    delta / (total + EPSILON)
)

engineered["theta_fraction"] = (
    theta / (total + EPSILON)
)

engineered["alpha_fraction"] = (
    alpha / (total + EPSILON)
)

engineered["beta_fraction"] = (
    beta / (total + EPSILON)
)

engineered["gamma_fraction"] = (
    gamma / (total + EPSILON)
)


# ============================================================
# CLEAN NUMERICAL VALUES
# ============================================================

feature_columns = engineered.columns.drop("Label")

engineered[feature_columns] = (
    engineered[feature_columns]
    .replace([np.inf, -np.inf], np.nan)
)

engineered[feature_columns] = (
    engineered[feature_columns]
    .fillna(0)
)


# ============================================================
# SAVE
# ============================================================

engineered.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

original_features = len(df.columns) - 1
new_features = len(engineered.columns) - 1
added_features = new_features - original_features


print("\n" + "=" * 70)
print("FEATURE ENGINEERING COMPLETED")
print("=" * 70)

print(
    f"\nOriginal features : {original_features}"
)

print(
    f"Final features    : {new_features}"
)

print(
    f"New features added: {added_features}"
)

print(
    f"\nOutput file:"
)

print(
    OUTPUT_FILE
)

print("\nNew engineered features:")

for column in engineered.columns:

    if column not in df.columns:

        print(
            " -",
            column
        )


print("\nFinal dataset shape:")

print(
    engineered.shape
)

print("\nDone.")