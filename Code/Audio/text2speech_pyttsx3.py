import pyttsx3
import pandas as pd
import os

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# Load Stimuli dataframe
csv_path = r'C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\English\English_Stimuli.csv'
stimuli_df = pd.read_csv(csv_path)

# Extract words and place into a list
word_list = stimuli_df['Word'].to_list()

# Directory to save the MP3 files
output_dir = r'C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Auditory\English\pyttsx3_MP3_Files'
os.makedirs(output_dir, exist_ok=True)

# Function to save speech to file
def save_speech_to_file(text, voice_id, filename):
    engine.setProperty('voice', voice_id)
    engine.save_to_file(text, filename)
    engine.runAndWait()

# Get available voices
voices = engine.getProperty('voices')

# Assuming the first voice is male and the second is female
male_voice_id = voices[0].id
female_voice_id = voices[1].id

# Generate and save MP3 files for each word
for word in word_list:
    male_filename = os.path.join(output_dir, f"{word}_male.mp3")
    female_filename = os.path.join(output_dir, f"{word}_female.mp3")
    
    save_speech_to_file(word, male_voice_id, male_filename)
    save_speech_to_file(word, female_voice_id, female_filename)

print("MP3 files have been generated and saved.")