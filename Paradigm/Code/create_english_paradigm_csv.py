import pandas as pd
import os

# File paths
visual_stimuli_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\English\English_Stimuli.csv"
audio_files_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Paradigm\Audio_Files_Google_Cloud"

# Load the visual stimuli CSV
visual_stimuli_df = pd.read_csv(visual_stimuli_path)

# Extract the necessary columns: 'Word' and 'Condition'
visual_stimuli_df = visual_stimuli_df[['Word', 'Condition']]

# Create lists to store the corresponding audio files
audio_male = []
audio_female = []

# Iterate through each word in the visual stimuli and find the corresponding audio files
for word in visual_stimuli_df['Word']:
    # Find files that start with the word in the audio directory
    matching_files = [f for f in os.listdir(audio_files_path) if f.startswith(word) and f.endswith('.wav')]
    
    if matching_files:
        # Initialize male and female audio variables
        male_audio = None
        female_audio = None
        
        for file in matching_files:
            if file.endswith(('_FEMALE_C.wav')):  # Female voice files
                female_audio = file
            elif file.endswith(('_MALE_D.wav')):  # Male voice files
                male_audio = file
        
        # Append the corresponding audio files to the lists
        audio_male.append(male_audio)
        audio_female.append(female_audio)
    else:
        # If no matching audio found, append None
        audio_male.append(None)
        audio_female.append(None)

# Add the audio columns to the DataFrame
visual_stimuli_df['Audio_Male'] = audio_male
visual_stimuli_df['Audio_Female'] = audio_female

# Save the updated DataFrame to a new CSV
output_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Paradigm\Stimuli\en_paradigm.csv"
visual_stimuli_df.to_csv(output_path, index=False)

print(f"Updated CSV saved to {output_path}")
