import os

# Get the project root directory dynamically
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define folder paths
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
API_DIR = os.path.join(BASE_DIR, "api")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")  # New upload folder

# Ensure necessary directories exist
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Path for resume CSV file
RESUME_CSV_PATH = os.path.join(DATA_DIR, "Resume_data.csv")

# Define file paths
PROCESSED_RESUMES_PATH = os.path.join(DATA_DIR, "processed_resumes.txt")
EXTRACTED_RESUMES_PATH = os.path.join(DATA_DIR, "extracted_resumes.txt")
TFIDF_VECTOR_PATH = os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl")
BERT_FEATURES_PATH = os.path.join(MODELS_DIR, "hybrid_features.pkl")
BEST_MODEL_PATH = os.path.join(MODELS_DIR, "best_model.pkl")
SELECTED_FEATURES_PATH = os.path.join(MODELS_DIR, "selected_features.pkl")  # Added selected features path

# Save paths for extracted features
ADV_CSV_PROCESSED_PATH = os.path.join(DATA_DIR, "processed_resume_data.csv")  # Save cleaned text
ADV_CSV_FEATURES_PATH = os.path.join(MODELS_DIR, "hybrid_csv_features.pkl")  # Save features
ADV_CSV_LABELS_PATH = os.path.join(MODELS_DIR, "csv_labels.pkl")  # Save category labels

print(" Config file loaded successfully!")
