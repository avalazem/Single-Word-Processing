import pandas as pd
import random
import os

# File paths
input_file = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\Stimuli\en_paradigm.csv"
output_dir = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\Stimuli\Subject_Sampled_Stimuli"

# Read the original CSV file into a DataFrame
df = pd.read_csv(input_file)

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Get a unique subject number (you can customize this if needed)
subject_number = "Subject_one"  # Change this to dynamically generate if needed

# Initialize an empty DataFrame to collect the sampled rows
sampled_data = pd.DataFrame()

# Initialize a list to keep track of which audio (male/female) is selected
audio_choices = []

# For each condition, sample 8 random words and alternate between male/female audio
for condition in df['Condition'].unique():
    condition_data = df[df['Condition'] == condition]
    sampled_condition_data = condition_data.sample(n=8, random_state=random.seed())
    
    # Alternate between male and female audio for the sampled data
    for i, row in sampled_condition_data.iterrows():
        word = row['Word']
        male_audio = row['Audio_Male']  # Use the audio file from the Audio_Male column
        female_audio = row['Audio_Female']  # Use the audio file from the Audio_Female column
        
        # Alternate audio between male and female
        if len(audio_choices) % 2 == 0:
            audio_choices.append(male_audio)  # Add male audio
        else:
            audio_choices.append(female_audio)  # Add female audio

    # Add the audio choices to the sampled data
    sampled_condition_data['Audio'] = audio_choices[-8:]  # Only take the last 8 added

    # Add the sampled condition data to the final DataFrame
    sampled_data = pd.concat([sampled_data, sampled_condition_data])

# Generate a random file name
output_file = os.path.join(output_dir, f"{subject_number}_en.csv")

# Save the sampled DataFrame to a new CSV with only 'Word', 'Condition', and 'Audio'
sampled_data[['Word', 'Condition', 'Audio']].to_csv(output_file, index=False)

print(f"New CSV with sampled words, conditions, and audio saved as: {output_file}")
