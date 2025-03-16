import pandas as pd
import joblib
import re
import sys
import os
import spacy
import contractions

from config import RESUME_CSV_PATH, ADV_CSV_PROCESSED_PATH, ADV_CSV_FEATURES_PATH, ADV_CSV_LABELS_PATH
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from feature_extraction import extract_features  # Import existing feature extraction function
from nltk.corpus import stopwords
from tqdm import tqdm

# Load CSV Data
df = pd.read_csv(RESUME_CSV_PATH)

# Load NLP Models
nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words("english"))

# Advanced Preprocessing Function
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = contractions.fix(text)  # Expand contractions ("don't" -> "do not")
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    
    # Tokenization, Stopword Removal, and Lemmatization
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.text not in stop_words]
    
    return " ".join(tokens)

# Apply Advanced Preprocessing with Progress Bar
print("🚀 Preprocessing resume text...")
df["Resume_str"] = [preprocess_text(text) for text in tqdm(df["Resume_str"])]

# Save Cleaned Text to CSV for Future Use
df.to_csv(ADV_CSV_PROCESSED_PATH, index=False)
print(f"✅ Cleaned Resume Text Saved: {ADV_CSV_PROCESSED_PATH}")

# Extract Features (TF-IDF + BERT)
print("🚀 Extracting features from processed resumes...")
features = extract_features(df["Resume_str"].tolist(), ADV_CSV_FEATURES_PATH)  # Now it saves separately

# Convert Categories to Numerical Labels
categories = df["Category"].astype("category").cat.codes

# Save Processed Data
joblib.dump(categories, ADV_CSV_LABELS_PATH)

print(f"✅ Advanced CSV Processing Complete! Features saved in {ADV_CSV_FEATURES_PATH}")
print(f"✅ Labels saved in {ADV_CSV_LABELS_PATH}")
