import re
import nltk
import spacy
import contractions
import joblib
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Load spaCy English model (Disable unused features for speed)
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

# Load NLTK stop words
stop_words = set(stopwords.words('english'))

# Function to clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-English characters
    return text.strip()

# Remove stop words
def remove_stopwords(text):
    words = word_tokenize(text)
    return " ".join([word for word in words if word not in stop_words])

# Expand contractions
def expand_contractions(text):
    return contractions.fix(text)

# Remove common resume headers
def remove_headers(text):
    headers = ["contact info", "references", "skills", "education", "experience"]
    for header in headers:
        text = re.sub(rf'\b{header}\b.*', '', text, flags=re.IGNORECASE)
    return text

# Apply lemmatization using spaCy (optimized with nlp.pipe)
def lemmatize_texts(texts):
    lemmatized_texts = []
    for doc in nlp.pipe(texts, batch_size=50):
        lemmatized_texts.append(" ".join([token.lemma_ for token in doc]))
    return lemmatized_texts

# Read extracted resumes from file
with open("extracted_resumes.txt", "r", encoding="utf-8") as f:
    resumes = f.readlines()

# ✅ Optimize Performance: Use Parallel Processing (Joblib)
def process_resume(resume):
    resume = clean_text(resume)
    resume = remove_headers(resume)
    resume = expand_contractions(resume)
    resume = remove_stopwords(resume)
    return resume  # Lemmatization is done separately in batch mode

# Process resumes in parallel (CPU multiprocessing)
processed_resumes = joblib.Parallel(n_jobs=-1)(joblib.delayed(process_resume)(resume) for resume in resumes)

# ✅ Apply fast lemmatization in batches
processed_resumes = lemmatize_texts(processed_resumes)

# Save cleaned resumes (overwrite old file)
with open("processed_resumes.txt", "w", encoding="utf-8") as f:
    for resume in processed_resumes:
        f.write(resume + "\n")

print("✅ FAST Resume Preprocessing Completed! Check 'processed_resumes.txt'.")
