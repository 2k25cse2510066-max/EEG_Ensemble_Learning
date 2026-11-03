import pandas as pd
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Input and output paths
input_file = PROJECT_ROOT / "dataset" / "EEG_Extracted_Features.csv"
output_file = PROJECT_ROOT / "dataset" / "EEG_Binary_Classification.csv"

# Load dataset
df = pd.read_csv(input_file)

print("========== ORIGINAL DATASET ==========")
print("Dataset Shape:", df.shape)
print("\nOriginal Class Distribution:")
print(df["Label"].value_counts())

# Define binary label mapping
label_mapping = {
    "Epileptic_No_Seizure": "Epileptic",
    "Epileptogenic_Region": "Epileptic",
    "Seizure": "Epileptic",
    "Healthy_Eyes_Open": "Non_Epileptic",
    "Healthy_Eyes_Closed": "Non_Epileptic"
}

# Create new binary label
df["Binary_Label"] = df["Label"].map(label_mapping)

# Check for unmapped labels
if df["Binary_Label"].isnull().any():
    print("\nUnmapped labels found:")
    print(df[df["Binary_Label"].isnull()]["Label"].unique())
    raise ValueError("Some labels were not mapped correctly.")

# Remove original five-class label
binary_df = df.drop(columns=["Label"])

# Save binary dataset
binary_df.to_csv(output_file, index=False)

print("\n========== BINARY DATASET ==========")
print("Binary Dataset Shape:", binary_df.shape)

print("\nBinary Class Distribution:")
print(binary_df["Binary_Label"].value_counts())

print("\nBinary Dataset saved successfully at:")
print(output_file)