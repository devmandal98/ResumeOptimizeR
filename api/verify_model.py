import joblib
import numpy as np
from config import ADV_CSV_FEATURES_PATH, ADV_CSV_LABELS_PATH, BEST_MODEL_PATH
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from scipy.sparse import csr_matrix

# ✅ Load trained model
print("🚀 Loading trained model...")
model = joblib.load(BEST_MODEL_PATH)

# ✅ Load selected features
important_indices = joblib.load("models/selected_features.pkl")

# ✅ Load dataset
X = joblib.load(ADV_CSV_FEATURES_PATH)
y = joblib.load(ADV_CSV_LABELS_PATH)

# ✅ Convert X to sparse format (Ensure consistency)
X = csr_matrix(X)

# ✅ Apply feature selection
X_selected = X[:, important_indices]

# ✅ Split Data (Same as Training)
_, X_test, _, y_test = train_test_split(X_selected, y, test_size=0.2, random_state=42, stratify=y)

# ✅ Predict with the model
y_pred = model.predict(X_test)

# ✅ Print Accuracy Report
print("✅ Model Verified: Classification Report")
print(classification_report(y_test, y_pred, zero_division=1))
