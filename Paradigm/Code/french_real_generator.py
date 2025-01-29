import pandas as pd
from wordfreq import zipf_frequency


# Load the combinations CSV file
input_csv_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\French\Morpholex-FR\Morpholex_FR.xlsx"

# Filter by condition
RXXS_df = pd.read_excel(input_csv_path, "0-1-0")
RXXC_df_1 = pd.read_excel(input_csv_path, "0-1-3")
#RXXC_df_2 = pd.read_excel(input_csv_path, "0-2-0")
RXXC_df_3 = pd.read_excel(input_csv_path, "0-1-1")
RXXC_df_4 = pd.read_excel(input_csv_path, "0-2-2")
#RXXC_df_5 = pd.read_excel(input_csv_path, "0-3-0")
RXXC_df_6 = pd.read_excel(input_csv_path, "1-1-0")
RXXC_df_7 = pd.read_excel(input_csv_path, "1-1-1")
RXXC_df_8 = pd.read_excel(input_csv_path, "1-1-2")
RXXC_df_9 = pd.read_excel(input_csv_path, "1-1-3")
RXXC_df_10 = pd.read_excel(input_csv_path, "1-2-0")
RXXC_df_11 = pd.read_excel(input_csv_path, "1-2-1")
RXXC_df_12 = pd.read_excel(input_csv_path, "2-1-0")
RXXC_df_13 = pd.read_excel(input_csv_path, "2-1-1")
RXXC_df_14 = pd.read_excel(input_csv_path, "2-1-2")
RXXC_df_15 = pd.read_excel(input_csv_path, "0-1-2")

# Combine all DataFrames
combined_df = pd.concat([RXXC_df_1, RXXC_df_3, RXXC_df_4, RXXC_df_6, RXXC_df_7, RXXC_df_8, RXXC_df_9, RXXC_df_10, RXXC_df_11, RXXC_df_12, RXXC_df_13, RXXC_df_14, RXXC_df_15])

# Replace 'item' column with 'Word'
combined_df.rename(columns={'item': 'Word'}, inplace=True)
RXXS_df.rename(columns={'item': 'Word'}, inplace=True)


# Extract the word in parentheses from the 'Lemma' column
combined_df['Lemma'] = combined_df['canon_segm'].str.extract(r'\((.*?)\)')
RXXS_df['Lemma'] = RXXS_df['canon_segm'].str.extract(r'\((.*?)\)')

# Select only the 'Word', 'prs', 'freq', and 'n_morpheme' columns
selected_columns_df = combined_df[['Word', 'Lemma', 'prs', 'freq', 'n_morphemes']]
RXXS_df = RXXS_df[['Word', 'Lemma', 'prs', 'freq', 'n_morphemes']]

# Calculate the word length and add it as a 'Length' column
selected_columns_df['Length'] = selected_columns_df['Word'].str.len()
RXXS_df['Length'] = RXXS_df['Word'].str.len()

# Calculate the Lemma Zipf frequency and add it as a 'Lemma_Zipf_Frequency' column for selected_columns_df
selected_columns_df['Lemma_Zipf_Frequency'] = selected_columns_df['Lemma'].apply(lambda word: zipf_frequency(word, 'fr'))
RXXS_df['Lemma_Zipf_Frequency'] = RXXS_df['Lemma'].apply(lambda word: zipf_frequency(word, 'fr'))

# Remove quotation marks from prs column
selected_columns_df['prs'] = selected_columns_df['prs'].str.replace("'", "")
RXXS_df['prs'] = RXXS_df['prs'].str.replace("'", "")

# Calculate the French Zipf frequency and add it as a 'Zipf_Frequency' column
selected_columns_df['Zipf_Frequency'] = selected_columns_df['Word'].apply(lambda word: zipf_frequency(word, 'fr'))
RXXS_df['Zipf_Frequency'] = RXXS_df['Word'].apply(lambda word: zipf_frequency(word, 'fr'))

# Remove rows with Zipf frequency of 0
selected_columns_df = selected_columns_df[selected_columns_df['Zipf_Frequency'] > 0]
RXXS_df = RXXS_df[RXXS_df['Zipf_Frequency'] > 0]

# Function to split DataFrame into low and high frequency based on Zipf frequency
def split_by_frequency(df):
    low_freq_df = df[df['Zipf_Frequency'] < 3.5]
    high_freq_df = df[df['Zipf_Frequency'] > 4.0]
    return low_freq_df, high_freq_df

# Split selected_columns_df into 4, 5, 6 length words and 8, 9, 10 length words
short_words_df = selected_columns_df[selected_columns_df['Length'].isin([4, 5, 6])]
long_words_df = selected_columns_df[selected_columns_df['Length'].isin([8, 9, 10])]

# Split RXXS_df into 4, 5, 6 length words and 8, 9, 10 length words
short_words_RXXS_df = RXXS_df[RXXS_df['Length'].isin([4, 5, 6])]
long_words_RXXS_df = RXXS_df[RXXS_df['Length'].isin([8, 9, 10])]

# Split each subset into high and low frequency halves
RSLC_df, RSHC_df = split_by_frequency(short_words_df)
RLLC_df, RLHC_df = split_by_frequency(long_words_df)
RSLS_df, RSHS_df = split_by_frequency(short_words_RXXS_df)
RLLS_df, RLHS_df = split_by_frequency(long_words_RXXS_df)


# Sort by length
RSLC_df = RSLC_df.sort_values(by='Length')
RSHC_df = RSHC_df.sort_values(by='Length')
RLLC_df = RLLC_df.sort_values(by='Length')
RLHC_df = RLHC_df.sort_values(by='Length')
RSLS_df = RSLS_df.sort_values(by='Length')
RSHS_df = RSHS_df.sort_values(by='Length')
RLLS_df = RLLS_df.sort_values(by='Length')
RLHS_df = RLHS_df.sort_values(by='Length')


# Save the DataFrames to CSV files
RSLC_df.to_csv(r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\French\Morpholex-FR\RSLC_samples.csv", index=False)
RSHC_df.to_csv(r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\French\Morpholex-FR\RSHC_samples.csv", index=False)
RLLC_df.to_csv(r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\French\Morpholex-FR\RLLC_samples.csv", index=False)
RLHC_df.to_csv(r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\French\Morpholex-FR\RLHC_samples.csv", index=False)
RSLS_df.to_csv(r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\French\Morpholex-FR\RSLS_samples.csv", index=False)
RSHS_df.to_csv(r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\French\Morpholex-FR\RSHS_samples.csv", index=False)
RLLS_df.to_csv(r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\French\Morpholex-FR\RLLS_samples.csv", index=False)
RLHS_df.to_csv(r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\French\Morpholex-FR\RLHS_samples.csv", index=False)

print("DataFrames saved to CSV files!")