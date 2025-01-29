import pandas as pd
from wordfreq import zipf_frequency
import random

# Define consonant categories
def categorize_consonants():
    """Returns a dictionary of French consonants categorized phonetically."""
    return {
        "stops": {
            "voiced": ["b", "d", "g"],
            "voiceless": ["p", "t", "k"]
        },
        "nasals": ["m", "n", "gn", "ng"],
        "fricatives": {
            "voiced": ["v", "z", "j"],
            "voiceless": ["f", "s", "ch"]
        },
        "liquids": ["l", "r"],
        "glides": ["w", "u", "y"]
    }
def replace_consonants(word, categories, num_replacements=2):
    """
    Replaces a specified number of consonants in the word with others from the same category.
    
    Args:
        word (str): The original word.
        categories (dict): The dictionary of consonant categories.
        num_replacements (int): Number of consonants to replace.
        
    Returns:
        str: The modified word with consonants replaced.
    """
    consonants = [char for char in word if any(char in subcat for subcat in categories.values())]
    if len(consonants) < num_replacements:
        num_replacements = len(consonants)  # Adjust if fewer consonants exist
    
    # Choose consonants to replace, ensuring no duplicates
    consonants_to_replace = random.sample(consonants, num_replacements)
    modified_word = word
    
    for consonant_to_replace in consonants_to_replace:
        for category, subcategories in categories.items():
            if isinstance(subcategories, dict):  # For voiced/voiceless distinctions
                for consonants in subcategories.values():
                    if consonant_to_replace in consonants:
                        replacements = [c for c in consonants if c != consonant_to_replace]
                        if replacements:
                            modified_word = modified_word.replace(consonant_to_replace, random.choice(replacements), 1)
                        break
            elif consonant_to_replace in subcategories:  # For non-distinction categories
                replacements = [c for c in subcategories if c != consonant_to_replace]
                if replacements:
                    modified_word = modified_word.replace(consonant_to_replace, random.choice(replacements), 1)
                break
    
    return modified_word

# Check if a word contains any consonants
def has_consonants(word, categories):
    """Checks if a word contains any consonants."""
    return any(char in subcat for subcat in categories.values() for char in word)

# Calculate the Levenshtein distance
def levenshtein_distance(s1, s2):
    """Calculates the Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

# Load data
input_csv_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\French\Morpholex-FR\Morpholex_FR.xlsx"
categories = categorize_consonants()

# Filter and process DataFrames
def process_dataframe(sheet_name):
    """Process a single sheet into a pseudoword DataFrame."""
    df = pd.read_excel(input_csv_path, sheet_name)
    df.rename(columns={'item': 'Word'}, inplace=True)
    df['Lemma'] = df['canon_segm'].str.extract(r'\((.*?)\)')
    df = df[['Word', 'Lemma', 'prs', 'n_morphemes']]
    df['prs'] = df['prs'].str.replace("'", "")
    df = df[df['Word'].apply(lambda word: has_consonants(word, categories))]
    df['Pseudoword'] = df['Word'].apply(lambda word: replace_consonants(word, categories))
    df['Length'] = df['Pseudoword'].str.len()
    df['Levenshtein_Distance'] = df.apply(lambda row: levenshtein_distance(row['Word'], row['Pseudoword']), axis=1)
    return df

# Process data from sheets
complex_df = pd.concat([
    process_dataframe(sheet)
    for sheet in ["0-1-3", "0-1-1", "0-2-2", "1-1-0", "1-1-1", "1-1-2", "1-1-3", 
                  "1-2-0", "1-2-1", "2-1-0", "2-1-1", "2-1-2", "0-1-2"]
])
simple_df = process_dataframe("0-1-0")

# Split and save
def split_and_save(df, lengths, output_path):
    """Split and save the DataFrame by word length."""
    sub_df = df[df['Length'].isin(lengths)].sort_values(by='Length')
    sub_df.to_csv(output_path, index=False)

#split_and_save(complex_df, [4, 5, 6], r"C:\Users\ali_a\Desktop\PSC_samples.csv")
#split_and_save(complex_df, [8, 9, 10], r"C:\Users\ali_a\Desktop\PLC_samples.csv")
#split_and_save(simple_df, [4, 5, 6], r"C:\Users\ali_a\Desktop\PSS_samples.csv")
#split_and_save(simple_df, [8, 9, 10], r"C:\Users\ali_a\Desktop\PLS_samples.csv")

#print("DataFrames saved to CSV files!")
