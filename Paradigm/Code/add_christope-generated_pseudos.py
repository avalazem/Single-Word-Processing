import pandas as pd
from wordfreq import top_n_list
from rapidfuzz import process
from Levenshtein import distance

# Import the pseudowords
input_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Pseudoword_Generation\pseudowords.txt"
pseudo_df = pd.read_csv(input_path, header=None)

# Create word column
pseudo_df.rename(columns={0: 'Word'}, inplace=True)

# Caclulate word length
pseudo_df['Word_Length'] = pseudo_df['Word'].apply(lambda x: len(x))

# Sort by word length
pseudo_df.sort_values(by = 'Word_Length', ascending= True, inplace=True)

# Calculate Levenshtein distance

french_words = set(top_n_list('fr', 50000))

# Define a function to calculate minimum Levenshtein distance
def min_levenshtein(word, lexicon):
    match, score, _ = process.extractOne(word, lexicon, scorer=distance)
    return score  # Minimum Levenshtein distance

pseudo_df["levenshtein_dist"] = pseudo_df['Word'].apply(lambda word: min_levenshtein(word, french_words))
pseudo_df["normalized_levenshtein_dist"] = pseudo_df.apply(lambda row: row['levenshtein_dist'] / row['Word_Length'], axis=1)

# Remove any with normalized levenshtein distance less than 0.2
pseudo_df = pseudo_df[pseudo_df['normalized_levenshtein_dist'] >= 0.2]

# Sort by Word_Length and then by levenshtein_dist within each Word_Length
pseudo_df = pseudo_df.sort_values(by=['Word_Length', 'levenshtein_dist'])

# Separate by condition (4, 5, 6, 7, 8  letters short, 7, 8, 9, 10, 11 letters long)
PSX_df = pseudo_df[pseudo_df['Word_Length'] <= 8]
PLX_df = pseudo_df[pseudo_df['Word_Length'] >= 8]

# Export 
PSX_output_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\French\Christophe_Generated_Pseudos\Christophe_PSX.csv"
PLX_output_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\French\Christophe_Generated_Pseudos\Christophe_PLX.csv"

PSX_df.to_csv(PSX_output_path, index= False)
PLX_df.to_csv(PLX_output_path, index= False)

# Test
print(pseudo_df.head())
