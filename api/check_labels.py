import joblib
import numpy as np
from collections import Counter
from config import ADV_CSV_LABELS_PATH, CATEGORY_MAPPING  # Import paths

# ✅ Load the numerical category labels
labels = joblib.load(ADV_CSV_LABELS_PATH)

# ✅ Get unique category numbers
unique_labels = np.unique(labels)

# ✅ Count occurrences of each category
label_counts = Counter(labels)

print("📌 Unique Job Categories Found in Dataset:\n")
for label in unique_labels:
    job_field = CATEGORY_MAPPING.get(label, "Unknown")  # Get job name, default to "Unknown" if missing
    count = label_counts[label]
    print(f"🔹 Category {label}: {job_field} → {count} resumes")
