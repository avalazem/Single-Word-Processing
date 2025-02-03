import pandas as pd
import pyphen
from phonemizer.phonemize import phonemize
import os

from phonemizer.backend.espeak.wrapper import EspeakWrapper
os.environ['PHONEMIZER_ESPEAK_PATH'] = r'C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\eSpeak\command_line'
# EspeakWrapper.set_library(r'C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\eSpeak\command_line\espeak.exe')



# Ensure eSpeak is accessible
os.environ['PATH'] += r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\eSpeak\command_line"

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


def get_phonemes(word):
    try:
        phonetic_representation = phonemize(word, language='fr', backend='espeak', strip=True)
        return phonetic_representation  # Return the IPA phonetic representation
    except Exception as e:
        print(f"Phonemizer failed for '{word}': {e}")
        return None


# Function to count phonemes
def count_phonemes(word):
    phonemes = get_phonemes(word)
    if phonemes:
        return len(phonemes.replace(" ", "").replace(".", ""))  # Remove spaces and dots to count phonemes
    return None

# Load the CSV file into a DataFrame
file_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Pseudoword_Generation\Christophe_Generated_Pseudos\Christophe_PLX.csv"
df = pd.read_csv(file_path)

# Ensure 'Word' column exists
if 'Word' not in df.columns:
    raise ValueError("The CSV file must contain a 'Word' column.")

# Add columns for syllables, phonemes, and their counts
#df['Syllables'] = df['Word'].apply(get_syllables)
df['Num_Syllables'] = df['Word'].apply(count_syllables)
#df['Phonemes'] = df['Word'].apply(get_phonemes)
df['Num_Phonemes'] = df['Word'].apply(count_phonemes)

# Save the updated DataFrame back to the CSV file
df.to_csv(file_path, index=False)
print(f"Updated DataFrame saved to {file_path}")

phonemize("bonjour", language='fr', backend='espeak', logger=True)
