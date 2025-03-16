import joblib
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.model_selection import train_test_split
from config import ADV_CSV_FEATURES_PATH, ADV_CSV_LABELS_PATH, BEST_MODEL_PATH
from xgboost import XGBClassifier

# ✅ Load extracted features & labels
X = joblib.load(ADV_CSV_FEATURES_PATH)
y = joblib.load(ADV_CSV_LABELS_PATH)

# ✅ Convert X to sparse format
X = csr_matrix(X)

# ✅ Split data first (Same as before)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# ✅ Train a temporary model to extract feature importances
print("🚀 Training temporary model to extract feature importance...")
temp_model = XGBClassifier()  # Use same model type
temp_model.fit(X_train, y_train)

# ✅ Feature Selection: Select Top 2000 Important Features
important_indices = np.argsort(temp_model.feature_importances_)[::-1][:2000]

# ✅ Apply feature selection
X_train_selected = X_train[:, important_indices]  # ✅ Use only selected features
X_test_selected = X_test[:, important_indices]

# ✅ Train final model on selected features
model = XGBClassifier(n_estimators=350, max_depth=5, learning_rate=0.0178, subsample=0.75, colsample_bytree=0.55)
model.fit(X_train_selected, y_train)

# ✅ Save selected features & re-trained model
joblib.dump(important_indices, "models/selected_features.pkl")  # ✅ Save correct feature indices
joblib.dump(model, "models/best_model.pkl")  # ✅ Save re-trained model

print("✅ Model trained on selected features and saved!")
