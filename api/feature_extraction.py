import joblib
import numpy as np
import os
from tqdm import tqdm
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
from config import PROCESSED_RESUMES_PATH, TFIDF_VECTOR_PATH, BERT_FEATURES_PATH  # Import paths

# ✅ Load cleaned resumes
with open(PROCESSED_RESUMES_PATH, "r", encoding="utf-8") as f:
    resumes = [line.strip() for line in f.readlines() if line.strip()]

# ✅ Optimized TF-IDF Vectorizer
vectorizer = TfidfVectorizer(max_features=5000, stop_words="english", ngram_range=(1, 2), dtype=np.float32)

# ✅ Convert resumes into TF-IDF features
print("🚀 Extracting TF-IDF features...")
tfidf_matrix = vectorizer.fit_transform(resumes)

# ✅ Load Pretrained BERT Model
bert_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# ✅ Convert resumes into BERT embeddings (Batch Processing for Performance)
BATCH_SIZE = 100
bert_embeddings = []

print("🚀 Extracting BERT embeddings...")
for i in tqdm(range(0, len(resumes), BATCH_SIZE), desc="Processing BERT"):
    batch = resumes[i : i + BATCH_SIZE]
    embeddings = bert_model.encode(batch)
    bert_embeddings.append(embeddings)

# Convert list of embeddings to numpy array
bert_matrix = np.vstack(bert_embeddings)

# ✅ Apply PCA for Dimensionality Reduction (Improves Speed)
print("🚀 Applying PCA for feature reduction...")
pca = PCA(n_components=256)
bert_reduced = pca.fit_transform(bert_matrix)

# ✅ Combine TF-IDF and BERT features
final_features = hstack([tfidf_matrix, bert_reduced])

# ✅ Save Features & Vectorizer for Future Use
joblib.dump(final_features, BERT_FEATURES_PATH)
joblib.dump(vectorizer, TFIDF_VECTOR_PATH)

print("✅ Hybrid Feature Extraction Completed!")
print(f"🔹 Features saved to '{BERT_FEATURES_PATH}'.")

def extract_features(resumes, save_path=None):
    """
    Extracts features from resume text using TF-IDF + BERT.
    If save_path is provided, it saves the extracted features to that file.
    """
    print("🚀 Extracting features for new resumes...")
    
    # ✅ Transform resumes using the already trained vectorizer
    tfidf_matrix = vectorizer.transform(resumes)

    # ✅ Generate BERT embeddings (batch processing)
    BATCH_SIZE = 100
    bert_embeddings = []
    for i in tqdm(range(0, len(resumes), BATCH_SIZE), desc="Processing BERT"):
        batch = resumes[i : i + BATCH_SIZE]
        embeddings = bert_model.encode(batch)
        bert_embeddings.append(embeddings)

    # Convert list of embeddings to numpy array
    bert_matrix = np.vstack(bert_embeddings)

    # ✅ Apply PCA for feature reduction
    bert_reduced = pca.transform(bert_matrix)

    # ✅ Combine TF-IDF and BERT features
    final_features = hstack([tfidf_matrix, bert_reduced])

    # ✅ Save if save_path is provided
    if save_path:
        joblib.dump(final_features, save_path)
        print(f"✅ Features saved to '{save_path}'")

    return final_features
