import pandas as pd
from wordfreq import top_n_list
from rapidfuzz import process
from Levenshtein import distance



# import
input_file_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\French\french_stimuli.xlsx"
sheet_name = "french_stimuli_pseudo_sampled_edited"

# read
pseudo_init_df = pd.read_excel(input_file_path, sheet_name)

# extract
pseudo_df = pseudo_init_df[['Word', 'Wordlength', 'Length', 'Morphology', 'Lexicality', 'Condition', 'number of phonemes', 'number of syllables']]

# rename
pseudo_df.rename(columns={'number of phonemes': 'num_phonemes'}, inplace = True)
pseudo_df.rename(columns={'number of syllables': 'num_syllables'}, inplace = True)

# prep to calc levenshtein:

   # load french corpus of most frequent 50k words
french_words = set(top_n_list('fr', 50000))

   # Define a function to calculate minimum Levenshtein distance
def min_levenshtein(word, lexicon):
    match, score, _ = process.extractOne(word, lexicon, scorer=distance)
    return score  # Minimum Levenshtein distance

# calc levenshtein
pseudo_df['levenshtein_dist'] = pseudo_df['Word'].apply(lambda word: min_levenshtein(word, french_words))

# same but normalized for word length
pseudo_df['normalized_levenshtein_dist'] = pseudo_df.apply(lambda row: row['levenshtein_dist'] / row['Wordlength'], axis=1)

# Move the 'Lexicality' column to the left of 'Length'
cols = pseudo_df.columns.tolist()
cols.insert(cols.index('Length'), cols.pop(cols.index('Lexicality')))
pseudo_df = pseudo_df[cols]

# TEst
print(pseudo_df.head())

# Export
output_file_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\French\french_stimuli_pseudo_sampled_edited.csv"
pseudo_df.to_csv(output_file_path, index=False)