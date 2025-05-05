import pandas as pd

df1 = pd.read_csv('data/processed/features.csv')
df2 = pd.read_csv('data/processed/features1.csv')

merged = pd.concat([df1, df2], ignore_index=True)

merged.to_csv('data/processed/features_combined.csv', index=False)
