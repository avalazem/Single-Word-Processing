import random
import pandas as pd
import numpy as np
import os
from pathlib import Path

def create_visual_cat_localizer(SUBJECT):
    csv_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Localizer\Stimuli\CSVs"
    
    block_reps=3
    INTERBLOCK_DURATION = 6000  # in ms
    STIM_DURATION = 100
    ONSET = 2000
    categories=['face', 'emoji', 'wordEF', 'wordEF', 'wordC', 'Mu']

    shuffled_categories = []
    localizer = []
    
    for _ in range(block_reps):
        temp = categories[:]
        random.shuffle(temp)
        # Ensure no consecutive repetitions between blocks
        while len(shuffled_categories) > 0 and shuffled_categories[-1] == temp[0]:
            random.shuffle(temp)
        # Ensure no consecutive repetitions within the block
        while any(temp[i] == temp[i + 1] for i in range(len(temp) - 1)):
            random.shuffle(temp)
        shuffled_categories.extend(temp)

    categories = shuffled_categories

    has_star = ([1] * len(categories)) + ([0] * len(categories) * (block_reps - 1))
    random.shuffle(has_star)

    stims_idx = [x + 1 for x in range(20)]
    onset = ONSET

    first_block = True
    for bloc_type in zip(categories, has_star):
        random.shuffle(stims_idx)
        stims = [f"{bloc_type[0]}{x:02}.png" for x in stims_idx]
        if bloc_type[1] == 1:   # add star
            pos = random.choice(range(1, len(stims)))
            stims[pos] = "star.png"
        if not first_block:
            onset += INTERBLOCK_DURATION - STIM_DURATION # adjusting for onset
        first_block = False
        for x in stims:
            localizer.append((onset, 'picture', x))
            #print((onset, x))
            onset += STIM_DURATION

    # Convert the localizer list to a Pandas DataFrame
    df = pd.DataFrame(localizer, columns=['onset', 'type', 'stim'])

    # Save the DataFrame to a CSV file
    df.to_csv(Path(csv_path) / f"{SUBJECT}_vis.csv", index=False)
    print("Visual Localizer CSV file created successfully.")



# Audio localizer

def create_audio_cat_localizer(SUBJECT):
    csv_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Localizer\Stimuli\CSVs"
    block_reps=2
    INTERBLOCK_DURATION = 6000  # in ms
    AUDIO_DURATION = 1000
    ONSET = 2000
    categories=['words', 'words', 'words', 'scrambled_words', 'music', 'natural_sounds']

    shuffled_categories = []
    localizer = []
    
    for _ in range(block_reps):
        temp = categories[:]
        random.shuffle(temp)
        # Ensure no consecutive repetitions between blocks
        while len(shuffled_categories) > 0 and shuffled_categories[-1] == temp[0]:
            random.shuffle(temp)
        # Ensure no consecutive repetitions within the block
        while any(temp[i] == temp[i + 1] for i in range(len(temp) - 1)):
            random.shuffle(temp)
        shuffled_categories.extend(temp)

    categories = shuffled_categories
    
    stims_idx = [x + 1 for x in range(10)]
    onset = ONSET
    
    
    first_block = True
    for bloc_type in zip(categories):
        random.shuffle(stims_idx)
        if bloc_type[0] == 'scrambled_words':
            AUDIO_DURATION = 2000  # in ms
        else:
            AUDIO_DURATION = 1000
            
        if bloc_type[0] == 'scrambled_words':
            stims = [f"{bloc_type[0]}{x:02}.wav" for x in stims_idx[:5]]  # Only 1-5 for scrambled_words
        else:
            stims = [f"{bloc_type[0]}{x:02}.wav" for x in stims_idx]
        
        if not first_block:
            onset += INTERBLOCK_DURATION
            
        first_block = False
        previous_block = bloc_type[0]  # Track the current block type
        
        for x in stims:
            localizer.append((onset, 'sound', x))
            onset += AUDIO_DURATION
            
     # Convert the localizer list to a Pandas DataFrame
    df = pd.DataFrame(localizer, columns=['onset', 'type', 'stim'])

    # Save the DataFrame to a CSV file
    df.to_csv(Path(csv_path) / f"{SUBJECT}_audio.csv", index=False)
    print("Audio Localizer CSV file created successfully.")
    
def create_speech_localizer(SUBJECT):
    # Define the directory and ensure it exists
    csv_dir = Path(r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\SWP_Pilot_1\localizer\speech_categories")
    csv_dir.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist

    # Define the input file path
    input_file = csv_dir / "sub1_speech.csv"
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    # Read the CSV file
    df = pd.read_csv(input_file)

    onset = 2000  # Initial onset time
    # Iterate through the DataFrame and update the 'onset' column
    for index in range(len(df)):
        df.at[index, 'onset'] = onset
        if df.at[index, 'type'] == 'picture':
            onset += 26000
        elif df.at[index, 'type'] == 'text' and index + 1 < len(df) and df.at[index + 1, 'type'] == 'picture':
            onset += 11000
        elif df.at[index, 'type'] == 'text' and index + 1 < len(df) and df.at[index + 1, 'type'] == 'text':
            onset += 5000

    # Define the output file path
    output_file = csv_dir / f"{SUBJECT}_speech.csv"

    # Save the updated DataFrame
    df.to_csv(output_file, index=False)
    print(f"Speech Localizer CSV file created successfully at: {output_file}")
    
    
#create_audio_cat_localizer('sub1')
#create_visual_cat_localizer('sub1')
create_speech_localizer('sub1')