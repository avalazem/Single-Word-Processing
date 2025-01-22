import spacy.symbols
import wordfreq 
import pandas as pd
import spacy
from wordfreq import zipf_frequency

#load csv
# csv_file_path = r'C:\Users\ali_a\Desktop\Single Word Processing Stage\Single Word Processing\Data\French Data\french_stimuli_real.csv'
# df_stimuli = pd.read_csv(csv_file_path)

# add lemmas from simple words
# df_stimuli.loc[df_stimuli['Morphology'] == 'simple','Lemma'] = df_stimuli['Word']

               
# calculate zipf frequecies of the lemmas, then add to a new column
# df_stimuli['Zipf Lemma Frequency'] = df_stimuli['Lemma'].apply(lambda lemma: zipf_frequency(lemma, 'fr'))

# test
#print(df_stimuli)

# export
#df_stimuli.to_csv(csv_file_path, index=False)


# Testing Lemma frequencies (English)
'''
word='vengeful'
freq = zipf_frequency(word,'en')
print(f"Word: '{word}'\nFrequency: '{freq}'")
'''
#duplicates = df_stimuli[df_stimuli['Word'].duplicated(keep=False)]
#print(duplicates)

# Testing Lemma frequencies (French)

word='Dévaluant'
freq = zipf_frequency(word,'fr')
print(f"Word: '{word}'\nFrequency: '{freq}'")
