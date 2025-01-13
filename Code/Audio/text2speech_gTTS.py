import pandas as pd
from gtts import gTTS
import os

# Paths
input_csv_path = r'C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\Test_Stimuli_en.csv'
output_audio_dir = r'C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\audio_files_wav'
output_csv_path = r'C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\Test_Stimuli_en.csv'

# Load the CSV file
df = pd.read_csv(input_csv_path)

# Ensure the output directory exists
os.makedirs(output_audio_dir, exist_ok=True)

# Function to generate audio file for a word
def generate_audio(word, output_dir):
    tts = gTTS(text=word, lang='en')
    audio_file_path = os.path.join(output_dir, f"{word}.wav")
    tts.save(audio_file_path)
    return audio_file_path

# Generate audio files and update the DataFrame
audio_file_paths = []
for word in df['Word']:
    audio_file_path = generate_audio(word, output_audio_dir)
    audio_file_paths.append(os.path.basename(audio_file_path))

# Add the Audio column to the DataFrame
df['Audio'] = audio_file_paths

# Save the updated DataFrame to the CSV file
df.to_csv(output_csv_path, index=False)

print(f"Audio files have been generated and saved to {output_audio_dir}")
print(f"CSV file has been updated and saved to {output_csv_path}")