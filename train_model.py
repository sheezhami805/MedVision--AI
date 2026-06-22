import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load Dataset
df = pd.read_csv("dataset/Hospital_billing_fraud_detection.csv")

print("Dataset Shape:", df.shape)

# Encode categorical columns
encoders = {}

categorical_cols = [
    "Procedure_Code",
    "Lab_Test",
    "Insurance_Claim",
    "Hospital_Department"
]

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# Encode Label
label_encoder = LabelEncoder()
df["Label"] = label_encoder.fit_transform(df["Label"])

# Features
X = df.drop("Label", axis=1)

# Target
y = df["Label"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluation
pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, pred))
print("\nClassification Report:")
print(classification_report(y_test, pred))

# Save model
joblib.dump(model, "models/fraud_model.pkl")
joblib.dump(encoders, "models/encoders.pkl")
joblib.dump(label_encoder, "models/label_encoder.pkl")

print("\nModel Saved Successfully!")