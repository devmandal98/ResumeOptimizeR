import joblib
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from config import ADV_CSV_FEATURES_PATH, ADV_CSV_LABELS_PATH, BEST_MODEL_PATH

# ✅ Load trained model & selected feature indices
print("🚀 Loading trained model and selected features...")
model = joblib.load(BEST_MODEL_PATH)
important_indices = joblib.load("models/selected_features.pkl")  # ✅ Load saved feature indices

# ✅ Load full extracted features & labels
X = joblib.load(ADV_CSV_FEATURES_PATH)
y = joblib.load(ADV_CSV_LABELS_PATH)

# ✅ Convert X to sparse format
X = csr_matrix(X)

# ✅ Apply feature selection BEFORE splitting (Important!)
X_selected = X[:, important_indices]  # ✅ Use only selected features

# ✅ Split data (Same as during training)
_, X_test, _, y_test = train_test_split(X_selected, y, test_size=0.2, random_state=42, stratify=y)

# ✅ Make predictions using trained model
y_pred = model.predict(X_test)

# ✅ Generate updated classification report
print("🔹 Updated Classification Report (Fixed Feature Selection, Sparse Format):")
print(classification_report(y_test, y_pred, zero_division=1))
