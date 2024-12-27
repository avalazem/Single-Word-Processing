import pandas as pd

# Load combined DataFrame
csv_path=r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/French Data/deliane_french_real/deliane_combined.csv'
combined_df = pd.read_csv(csv_path)

# (Future Ali adding pseudos as well) (requires mods I removed but just remove Frequency, replacecombined_df, and replace export csv :)
pseudo_csv_path = r'C:\Users\ali_a\Desktop\Single Word Processing Stage\Single Word Processing\Data\French Data\french_stimuli_pseudo.csv'
pseudo_df= pd.read_csv(pseudo_csv_path)

# Function to get random samples based on the condition and wordlength
def get_samples(df, condition, wordlength):

    # Filter the DataFrame by the specific condition and wordlength while excluding medium 
    condition_df = df[(df['Condition'] == condition) & (df['Wordlength'] == wordlength) & (df['Frequency'] != 'medium')]
    
    # If there are enough entries, sample 5 random rows, otherwise take all
    if len(condition_df) >= 5:
        return condition_df.sample(n=5, random_state=42)
    else:
        return condition_df

# List to collect the sampled DataFrames
sampled_dataframes = []

# Get the unique conditions in the DataFrame
conditions = combined_df['Condition'].unique()

# For each condition, sample 5 words for each wordlength (4, 5, 6, 7, 8, 9, 10)
for condition in conditions:
    for wordlength in range(4, 11):  # Wordlengths from 4 to 10
        sampled_dataframes.append(get_samples(combined_df, condition, wordlength))

# Concatenate all the sampled DataFrames into one DataFrame
final_sampled_df = pd.concat(sampled_dataframes, ignore_index=True)

# Save the final DataFrame with samples to a new CSV

#csv_output_path=r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/French Data/deliane_french_real/french_stimuli_real.csv'

#final_sampled_df.to_csv(csv_output_path, index=False)
#print("Samples taken and saved!")

