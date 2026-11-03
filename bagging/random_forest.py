import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

# ==============================
# 1. Load dataset
# ==============================

file_path = "dataset/EEG_Engineered_Features.csv"
df = pd.read_csv(file_path)

print("Dataset Loaded Successfully")
print("Dataset Shape:", df.shape)

# ==============================
# 2. Separate features and target
# ==============================

X = df.drop("Label", axis=1)
y = df["Label"]

# ==============================
# 3. Same train-test split
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining Samples:", len(X_train))
print("Testing Samples:", len(X_test))

# ==============================
# 4. Create Random Forest model
# ==============================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

# ==============================
# 5. Train model
# ==============================

print("\nTraining Random Forest...")
model.fit(X_train, y_train)

print("Training Completed!")

# ==============================
# 6. Make predictions
# ==============================

y_pred = model.predict(X_test)

# ==============================
# 7. Calculate accuracy
# ==============================

accuracy = accuracy_score(y_test, y_pred)

print("\n========== RANDOM FOREST RESULTS ==========")
print(f"Accuracy: {accuracy * 100:.2f}%")

# ==============================
# 8. Classification report
# ==============================

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# ==============================
# 9. Confusion matrix
# ==============================

cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)

# ==============================
# 10. Plot confusion matrix
# ==============================

fig, ax = plt.subplots(figsize=(10, 8))

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=model.classes_
)

disp.plot(
    ax=ax,
    values_format="d",
    cmap="Blues",
    colorbar=True
)

ax.set_title(
    "Random Forest - 5-Class EEG Confusion Matrix",
    fontsize=18,
    pad=20
)

ax.set_xlabel("Predicted Label", fontsize=14)
ax.set_ylabel("Actual Label", fontsize=14)

ax.tick_params(axis="both", labelsize=11)

plt.tight_layout()

plt.savefig(
    "results/random_forest_engineered_confusion_matrix.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()