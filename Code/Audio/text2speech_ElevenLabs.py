from elevenlabs.client import ElevenLabs
import pandas as pd
import os
import random

# Set API key here
api_key = "sk_6cf73c0af9252d8c1f456b175541b23fc1d4882dd8cde913"

# Initialize the client
client = ElevenLabs(api_key=api_key)

# Load Stimuli dataframe
csv_path = r'C:\Users\ali_a\Desktop\Single Word Processing Stage\Single Word Processing\Data\English Data\English_Stimuli.csv'
stimuli_df = pd.read_csv(csv_path)

# Extract words and place into a list
word_list = stimuli_df['Word'].to_list()

# Directory to save the MP3 files
output_dir = r'C:\Users\ali_a\Desktop\Single Word Processing Stage\Single Word Processing\Data\English Data\ElevenLabs_MP3_Files'
os.makedirs(output_dir, exist_ok=True)

# Define voices
voices = [
    {"id": "9BWtsMINqrJLrRacOk9x", "name": "Aria"},  # Example female voice
    {"id": "cjVigY5qzO86Huf0OWal", "name": "Eric"}   # Example male voice
]

# Generate and save MP3 files for each word
for word in word_list:
    # Randomly choose a voice
    voice = random.choice(voices)
    audio_generator = client.text_to_speech.convert(
        text=word,
        voice_id=voice["id"],
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    
    # Generate and save the audio file
    output_path = os.path.join(output_dir, f"{word}_{voice['name']}.mp3")
    with open(output_path, 'wb') as f:
        for chunk in audio_generator:
            f.write(chunk)
    print(f"Saved {output_path} with voice {voice['name']}")

print("All words have been converted to MP3 files with a mix of male and female voices.")