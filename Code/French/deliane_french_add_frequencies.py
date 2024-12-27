import pandas as pd
from wordfreq import zipf_frequency



# Load combined DataFrame
csv_path=r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/French Data/deliane_french_real/deliane_combined.csv'
combined_df = pd.read_csv(csv_path)

# Function to get the Zipf frequency of a word
def get_zipf_frequency(word):
    return zipf_frequency(word, 'fr')  

# Apply the function to the 'Word' column
combined_df['Zipf Frequency'] = combined_df['Word'].apply(get_zipf_frequency)

# Create a 'Frequency' column based on Zipf frequencies
combined_df['Frequency'] = combined_df['Zipf Frequency'].apply(
    lambda x: 'low' if x < 3.5 else ('high' if x > 4 else 'medium') if x is not None else None
)

# Drop the extra 'Frequency' column (if exists) after calculating Zipf frequency
combined_df = combined_df.drop(columns=['Frequency'], errors='ignore')

# Save the updated DataFrame with the Zipf Frequency column

#combined_df.to_csv(csv_path, index=False)  # Replace with your desired output file name

print("Zipf Frequency column added and data saved to final_with_zipf.csv")
