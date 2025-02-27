import spacy 
import pandas as pd

# Load the sample csv data into a dataframe
csv_file_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\French\French_Reals_Filtered.csv"
df_stimuli = pd.read_csv(csv_file_path)

# Load spacy English model
#nlp = spacy.load('en_core_web_sm')  

# Load spacy French model
nlp = spacy.load('fr_core_news_sm')

# Function to get lemma from words

def get_lemma(word):
    return nlp(word)[0].lemma_ 
# nlp returns a doc of tokens, 0 is the first (only one token since one word) and lemma takes the lemma of it

df_stimuli['Lemma'] = df_stimuli['Word'].apply(get_lemma)
df_lemmas = df_stimuli[['Lemma']]
print(df_lemmas)
csv_output_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\French\French_Reals_Filtered_Lemmas.csv"
df_lemmas.to_csv(csv_output_path, index=False)
print("Lemmas Succesfully Added to French_Reals_Filtered_Lemmas.csv")
