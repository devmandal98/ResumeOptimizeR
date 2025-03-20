import joblib
import numpy as np
import spacy
import re
from config import BEST_MODEL_PATH, TFIDF_VECTOR_PATH, SELECTED_FEATURES_PATH, CATEGORY_MAPPING
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

# ✅ Load the trained model and vectorizer
print("🚀 Loading Model & Vectorizer...")
model = joblib.load(BEST_MODEL_PATH)
vectorizer = joblib.load(TFIDF_VECTOR_PATH)
selected_features = joblib.load(SELECTED_FEATURES_PATH)

# ✅ Load NLP Models
nlp = spacy.load("en_core_web_sm")
bert_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# ✅ Text Preprocessing Function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    
    # Lemmatization
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc]
    
    return " ".join(tokens)

# ✅ Feature Extraction Function
def extract_features(text):
    text = preprocess_text(text)
    
    # TF-IDF Features
    tfidf_features = vectorizer.transform([text]).toarray()

    # BERT Embeddings
    bert_embedding = bert_model.encode([text])

    # Combine Features
    final_features = np.hstack([tfidf_features, bert_embedding])

    # Select Important Features
    final_features_selected = final_features[:, selected_features]
    
    return final_features_selected

# ✅ Prediction Function (Returns Top 3 Categories & Confidence Scores)
def predict_category(resume_text):
    features = extract_features(resume_text)
    
    # Get probability scores for all categories
    probabilities = model.predict_proba(features)[0]

    # Get top 3 categories
    top_indices = np.argsort(probabilities)[-3:][::-1]
    top_categories = [CATEGORY_MAPPING[int(idx)] for idx in top_indices]
    confidence_scores = [round(float(probabilities[idx] * 100), 2) for idx in top_indices]  # ✅ Convert NumPy to Python types

    return [{"Category": category, "Confidence": f"{confidence}%"} for category, confidence in zip(top_categories, confidence_scores)]
