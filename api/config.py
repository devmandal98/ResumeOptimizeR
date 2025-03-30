import os

# Get the project root directory dynamically
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CATEGORY_MAPPING = {
    0: "HR",
    1: "Software Engineer",
    2: "Data Scientist",
    3: "Marketing",
    4: "Finance",
    5: "Healthcare",
    6: "Legal",
    7: "Education",
    8: "Sales",
    9: "Engineering",
    10: "Operations",
    11: "Design",
    12: "Customer Support",
    13: "Content Writing",
    14: "Product Management",
    15: "Business Development",
    16: "Consulting",
    17: "Research",
    18: "Administrative",
    19: "Manufacturing",
    20: "Retail",
    21: "Government",
    22: "Hospitality",
    23: "Other",
    24: "Cybersecurity",   # Added new category
    25: "Blockchain Developer",
    26: "Cloud Engineer",
    27: "Robotics Engineer",
    28: "Teaching", # Added new category
    29: "AI/ML Engineer",
    30: "Healthcare AI Specialist",
    31: "Business Analyst"
}

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
