import pandas as pd
from phonemizer.phonemize import phonemize
import pyphen
import os

# Set the eSpeak path
os.environ['PHONEMIZER_ESPEAK_LIBRARY'] = "C:/Program Files/eSpeak NG/libespeak-ng.dll"
os.environ['PHONEMIZER_ESPEAK_PATH'] = "C:/Program Files/eSpeak NG"

# Ensure eSpeak is accessible
os.environ['PATH'] += os.pathsep + "C:/Users/ali_a/Desktop/Single_Word_Processing_Stage/Single_Word_Processing/Code/eSpeak/command_line/espeak.exe"

def phonemize_word(word):
    try:
        phonetic_representation = phonemize(word, language='fr-fr', backend='espeak', strip=True)
        return phonetic_representation
    except Exception as e:
        print(f"Phonemizer failed for '{word}': {e}")
        return None

# Method 1: Count Characters
def phoneme_length(phonemes):
    if phonemes:
        return len(phonemes)  # Return the number of characters
    else:
        return 0
    
# Initialize Pyphen for French syllable splitting
dic = pyphen.Pyphen(lang='fr_FR')

# Function to split word into syllables and return the syllable string
def get_syllables(word):
    if isinstance(word, str):
        syllables = dic.inserted(word)
        return syllables  # Return the syllables as a string
    return None

# Function to count syllables
def count_syllables(word):
    syllables = get_syllables(word)
    if syllables:
        return len(syllables.split('-'))  # Count the number of syllables
    return None






# Read the CSV file
input_csv_path = r"C:\Users\ali_a\Downloads\French_Stimuli_Options.xlsx"
sheet_page = "RSHS_samples"
df = pd.read_excel(input_csv_path, sheet_page)

# Ensure 'Word' column exists
if 'Word' not in df.columns:
    raise ValueError("The CSV file must contain a 'Word' column.")

# Add a column for phonemes
df['Phonemes'] = df['Word'].apply(phonemize_word)

# Add a column for the length of phonemes
df['Phoneme_Length'] = df['Phonemes'].apply(phoneme_length)

# Add a column for the number of syllables
df['n_syllables'] = df['Word'].apply(count_syllables)

# Add a column for the difference between Phoneme_Length and n_syllables
df['Difference'] = df['Phoneme_Length'] - df['n_syllables']

# Move 'Length' to the left of 'prs'
cols = df.columns.tolist()
if 'Length' in cols and 'prs' in cols:
    cols.insert(cols.index('prs'), cols.pop(cols.index('Length')))
    df = df[cols]

# Move 'n_morphemes' to the left of 'n_syllables'
cols = df.columns.tolist()
if 'n_morphemes' in cols and 'n_syllables' in cols:
    cols.insert(cols.index('n_syllables'), cols.pop(cols.index('n_morphemes')))
    df = df[cols]

# Save the updated DataFrame back to csv file
output_path = r"C:\Users\ali_a\Downloads\RSHS_samples.csv"
df.to_csv(output_path, index=False)
print(f"Updated DataFrame saved to {output_path}")
