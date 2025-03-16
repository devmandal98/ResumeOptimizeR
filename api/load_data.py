import pandas as pd

# Load resume dataset
df = pd.read_csv("resume_data.csv")  # Load CSV file

# Print dataset information
print("Dataset Information:\n", df.info())

# Display first 5 rows
print("\nFirst 5 Rows:\n", df.head())

# Check for missing values
print("\nMissing Values:\n", df.isnull().sum())

# Count unique job categories
print("\nUnique Job Categories:\n", df["Category"].value_counts())
