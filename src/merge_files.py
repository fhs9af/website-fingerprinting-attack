import pandas as pd

# Load both CSVs
df1 = pd.read_csv('data/processed/features.csv')
df2 = pd.read_csv('data/processed/features1.csv')

# Concatenate them vertically
merged = pd.concat([df1, df2], ignore_index=True)

# Save to a new CSV
merged.to_csv('data/processed/features_combined.csv', index=False)
