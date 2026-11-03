import pandas as pd
from sklearn.model_selection import train_test_split

# Load dataset
file_path = "dataset/EEG_Extracted_Features.csv"
df = pd.read_csv(file_path)

print("========== DATASET INFORMATION ==========")
print("Dataset Shape:", df.shape)

# Separate features and target
X = df.drop("Label", axis=1)
y = df["Label"]

print("\nFeatures Shape:", X.shape)
print("Target Shape:", y.shape)

print("\nOriginal Class Distribution:")
print(y.value_counts())

# Train-test split
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

print("\nTrain-Test Split Completed Successfully!")