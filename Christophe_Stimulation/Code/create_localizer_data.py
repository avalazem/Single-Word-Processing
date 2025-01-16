import pandas as pd
import os

# Paths
audio_files_path = r'C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\Stimuli\reversed_audio_files_wav'
paradigm_csv_path = r'C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\Stimuli\en_paradigm.csv'
output_csv_path = r'C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\Stimuli\Localizer_en.csv'

# Load the paradigm data
paradigm_df = pd.read_csv(paradigm_csv_path)

# Get the list of audio files
audio_files = [f for f in os.listdir(audio_files_path) if f.endswith('.wav')]

# Extract the word from the audio file name and create a DataFrame
audio_df = pd.DataFrame({
    'Stimuli': audio_files,
    'Word': [f.split('_')[1] for f in audio_files],
    'Stimuli Type': ['Audio'] * len(audio_files)
})

# Merge with paradigm data to get conditions
merged_df = pd.merge(audio_df, paradigm_df, on='Word')

# Ensure every condition is covered, with no more than two of each
selected_df = pd.DataFrame()
for condition in merged_df['Condition'].unique():
    condition_df = merged_df[merged_df['Condition'] == condition]
    selected_df = pd.concat([selected_df, condition_df.sample(min(2, len(condition_df)))])

# If we have more than 15, randomly select 15 (change to more if needed)
if len(selected_df) > 15:
    selected_df = selected_df.sample(15)

# Save the selected DataFrame to a CSV file
selected_df[['Stimuli', 'Stimuli Type']].to_csv(output_csv_path, index=False)

print(f"CSV file has been created and saved to {output_csv_path}")