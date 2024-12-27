import pandas as pd

# Load combined DataFrame
csv_path=r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/French Data/deliane_french_real/deliane_combined.csv'
combined_df = pd.read_csv(csv_path)

# Create a new 'Condition' column based on the given conditions
combined_df['Condition'] = combined_df.apply(lambda row: 
    ('R' if row['Lexicality'] == 'real' else 'P') + 
    ('S' if row['Length'] == 'short' else 'L') + 
    ('L' if row['Frequency'] == 'low' else 'H') + 
    ('S' if row['Morphological Complexity'] == 'simple' else 'C'), axis=1)

# Save the updated DataFrame to a new CSV
combined_df.to_csv(csv_path, index=False)

print("Condition column added and saved!")
