import spacy 
import pandas as pd

# Load the sample csv data into a dataframe
csv_file_path = r'C:\Users\ali_a\Desktop\Single Word Processing Stage\Single Word Processing\Data\French Data\robin_french_stimuli_real_annotated.csv'
df_stimuli = pd.read_csv(csv_file_path)

# Load spacy English model
#nlp = spacy.load('en_core_web_sm')  

# Load spacy French model
nlp= spacy.load('fr_core_news_lg')

# Function to get lemma from words

def get_lemma(word):
    return nlp(word)[0].lemma_ 
# nlp returns a doc of tokens, 0 is the first (only one token since one word) and lemma takes the lemma of it

df_stimuli['Lemma'] = df_stimuli['Word'].apply(get_lemma)
print(df_stimuli)
df_stimuli.to_csv(csv_file_path, index=False)
print("Lemmas Succesfully Added to robin_french_stimuli_real_annotated.csv")
