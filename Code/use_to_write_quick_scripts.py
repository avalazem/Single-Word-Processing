import pandas as pd
from phonemizer.phonemize import phonemize
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

# Read the CSV file
input_csv_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Pseudoword_Generation\Christophe_Generated_Pseudos\Christophe_PSX.csv"
df = pd.read_csv(input_csv_path)

# Ensure 'Word' column exists
if 'Word' not in df.columns:
    raise ValueError("The CSV file must contain a 'Word' column.")

# Add a column for phonemes
df['Phonemes'] = df['Word'].apply(phonemize_word)

# Add a column for the length of phonemes
df['Phoneme_Length'] = df['Phonemes'].apply(phoneme_length)

# Save the updated DataFrame back to the CSV file
df.to_csv(input_csv_path, index=False)
print(f"Updated DataFrame saved to {input_csv_path}")

# Test the function with "bonjour"
phonemized = phonemize_word("bonjour")
phoneme_len = phoneme_length(phonemized)
print(f"Phonemized version of 'bonjour': {phonemized}, Length: {phoneme_len}")