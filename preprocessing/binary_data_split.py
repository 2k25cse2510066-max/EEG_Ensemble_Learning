import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Dataset path
file_path = PROJECT_ROOT / "dataset" / "EEG_Binary_Classification.csv"

# Load dataset
df = pd.read_csv(file_path)

print("========== BINARY DATASET INFORMATION ==========")
print("Dataset Shape:", df.shape)

# Separate features and target
X = df.drop("Binary_Label", axis=1)
y = df["Binary_Label"]

print("\nFeatures Shape:", X.shape)
print("Target Shape:", y.shape)

print("\nOriginal Class Distribution:")
print(y.value_counts())

# Stratified train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\n========== TRAIN / TEST SPLIT ==========")
print("Training samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])

print("\nTraining Class Distribution:")
print(y_train.value_counts())

print("\nTesting Class Distribution:")
print(y_test.value_counts())

print("\nBinary Train-Test Split Completed Successfully!")