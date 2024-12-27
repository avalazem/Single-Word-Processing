import pandas as pd
from Levenshtein import distance
from nltk.corpus import words
'''
# Step 1: Load the English lexicon (e.g., from nltk or a separate file)
try:
    # Ensure the NLTK word list is downloaded
    from nltk import download
    download('words')
except ImportError:
    raise ImportError("NLTK is required for loading English words. Install it using `pip install nltk`.")
'''

# Put English lexicon (~50k words) into a set
english_words = set(words.words())

# Step 2: Load the CSV file
input_csv = r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/English Data/english_sample_stimuli_pseudos.csv'
df = pd.read_csv(input_csv)

# Step 3: Define a function to calculate minimum Levenshtein distance
def min_levenshtein(word, lexicon):
    return min(distance(word, lex_word) for lex_word in lexicon) # loops through all lex_word s in lexicon

# Step 4: Calculate the minimum distance for each word in the dataframe
df['Min Levenshtein Distance'] = df['Word'].apply(lambda w: min_levenshtein(w, english_words))

# Step 5: Save the updated dataframe to a new CSV file
output_csv = r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/English Data/english_sample_stimuli_pseudos.csv'
df.to_csv(output_csv, index=False)
print(f"Output saved to {output_csv}")

'''
# To test individual words
word = 'lauly'
min_distance = min_levenshtein(word, english_words)
print(min_distance)
'''