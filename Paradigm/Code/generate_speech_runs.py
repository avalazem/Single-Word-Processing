import pandas as pd
import random
import os
import numpy as np
from collections import defaultdict

# Function to generate a 50/50 gender list

def generate_gender_list(n_entries):
    # Create an equal split of 'M' and 'F'
    half = n_entries // 2
    gender_list = ['M'] * half + ['F'] * half

    # If n_entries is odd, randomly add one more 'M' or 'F'
    if n_entries % 2 == 1:
        gender_list.append(random.choice(['M', 'F']))
        print("Warning: Odd Number of Stimuli - won't be 50/50!")
        
    # Shuffle the list for randomness
    random.shuffle(gender_list)

    return gender_list

# Function to merge additional columns from English_Stimuli.csv
def merge_additional_columns(df, stimuli_path):
    # Read the English_Stimuli.csv file
    stimuli_df = pd.read_csv(stimuli_path)

    # Select the required columns
    columns_to_merge = ['Word', 'Zipf Lemma Frequency', 'Lemma', 'Zipf Frequency', 'Part of Speech','Morphology', 'Length', 'Lexicality']
    stimuli_df = stimuli_df[columns_to_merge]


    # Merge the DataFrame with the existing DataFrame based on the 'Word' column
    merged_df = pd.merge(df, stimuli_df, on='Word', how='left')

    # Reorder the columns to place the specified columns to the right of 'Word'
    condition_index = merged_df.columns.get_loc('Word')
    new_order = merged_df.columns.tolist()
    for col in columns_to_merge[1:]:
        new_order.insert(condition_index + 1, new_order.pop(new_order.index(col)))
    merged_df = merged_df[new_order]

    # Replace Morphology with Morphological Complexity
    merged_df.rename(columns={'Morphology': 'Morphological Complexity'}, inplace=True)
    
    return merged_df

# Function to update run type and assign audio files based on gender
def assign_audio_gender(df, n_stimuli):
    # Generate gender list
    gender_list = generate_gender_list(n_stimuli)

    # Assign Audio based on gender list
    df['Audio File'] = [row.Audio_Male if gender == 'M' else row.Audio_Female for row, gender in zip(df.itertuples(), gender_list)]

    # Set no value if Input Modality is not Audio
    df.loc[df['Input Modality'] != 'Audio', 'Audio File'] = None

    # Drop the Audio_Male and Audio_Female columns
    df.drop(columns=['Audio_Male', 'Audio_Female'], inplace=True)

    # Reorder columns to place Audio to the left of Jitter_Duration
    columns = df.columns.tolist()
    audio_index = columns.index('Audio File')
    input_modality_index = columns.index('Trial Duration')
    columns.insert(input_modality_index, columns.pop(audio_index))
    df = df[columns]
    
    # Reorder columns to place Condtion to the left of 'Part of Speech
    columns = df.columns.tolist()
    condition_index = columns.index('Condition')
    input_modality_index = columns.index('Part of Speech')
    columns.insert(input_modality_index, columns.pop(condition_index))
    df = df[columns]
    
    return df

# Define function to assign jitter durations based on an even distribtion

def assign_jitter_durations(n_stimuli, mean_soa=5, step=0.5, n_durations=5):
    # Generate evenly spaced duration values
    durations = [mean_soa - step * (i - (n_durations - 1) / 2) for i in range(n_durations)]

    # Compute number of times each duration should be assigned
    base_repeats = n_stimuli // n_durations  # Even distribution
    remainder = n_stimuli % n_durations  # Leftover stimuli

    # Create the duration list
    assigned_durations = durations * base_repeats + [mean_soa] * remainder  # Add mean for remainder cases

    # Shuffle for randomness
    np.random.shuffle(assigned_durations)

    # Check sum (use np.isclose to avoid floating-point errors)
    assert np.isclose(sum(assigned_durations), n_stimuli * mean_soa, atol=1e-6), \
        "Sum of durations does not match the total required duration"

    return assigned_durations


def create_subject_csvs(input_csv, output_dir, stimuli_path, subject_name):
    # Load the CSV
    df = pd.read_csv(input_csv)

    # Ensure required columns exist
    required_columns = {"Word", "Condition", "Audio_Male", "Audio_Female"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"CSV must contain the columns: {required_columns}")

    # Get unique conditions
    conditions = df["Condition"].unique()

    # Store dataframes for the 6 runs
    run_dataframes = []

    for i in range(3):  # We need 3 mutually exclusive sets
        ws_list = []
        as_list = []

        for condition in conditions:
            # Select 5 words for this batch
            condition_words = df[df["Condition"] == condition].copy()
        
            
            if len(condition_words) < 15:
                raise ValueError(f"Not enough words in condition {condition}, need at least 15.")

            # Select 5 words for this batch
            selected_words = condition_words.iloc[i*5:(i+1)*5]  # Take 5 words
            ws_list.append(selected_words)  # Store in ws list
            as_list.append(selected_words.copy())  # Copy for as list

        # Create two dataframes, one for ws and one for as
        ws_df = pd.concat(ws_list, ignore_index=True)
        as_df = pd.concat(as_list, ignore_index=True)

        # Shuffle the entire DataFrame to mix conditions & words
        ws_df = ws_df.sample(frac=1, random_state=None).reset_index(drop=True)
        as_df = as_df.sample(frac=1, random_state=None).reset_index(drop=True)

        # Assign trial durations (Jitter Duration + 0.5 fixation) IMPORTANT TO SUBTRACT IN SCRIPT!!!
        n_stimuli = len(ws_df) # Same length for both ws and as
        ws_df["Trial Duration"] = assign_jitter_durations(n_stimuli)
        as_df["Trial Duration"] = assign_jitter_durations(n_stimuli)

        # Add additional information from original csv
        ws_df = merge_additional_columns(ws_df, stimuli_path)  # Merge additional columns
        as_df = merge_additional_columns(as_df, stimuli_path)  # Merge additional columns


        # Assign run type
        ws_df["Input Modality"] = "Visual"
        ws_df["Output Modality"] = "Speech"

        as_df["Input Modality"] = "Audio"
        as_df["Output Modality"] = "Speech"
        
        print(as_df.head())
        # Adjust audio to 50/50 Male/Female distribution
        as_df = assign_audio_gender(as_df, len(as_df))  # Update run type and assign audio
        ws_df = assign_audio_gender(ws_df, len(ws_df))  # Update run type and assign audio


        # Append them to run_dataframes
        run_dataframes.append(ws_df)
        run_dataframes.append(as_df)
    
       
    # Randomize the run indices (so runs aren't always in a set order)
    run_indices = np.random.permutation(6) + 1  # Generate 1-6 in random order

    # Save each dataframe with assigned run number
    for idx, run_df in enumerate(run_dataframes):
        run_filename = f"{subject_name}_Run_{run_indices[idx]}.csv"
        output_file = os.path.join(output_dir, run_filename)
        run_df.to_csv(output_file, index=False)
        print(f"Saved {run_filename}")

 
# Validate to ensure no mistakes (sanity check)
def validate_runs(subject_name, base_dir= r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Paradigm\Stimuli\Subject_Sampled_Stimuli"):
    run_files = [os.path.join(base_dir, f"{subject_name}_Run_{i}.csv") for i in range(1, 7)]
    run_data = {}

    # Load all runs
    for file in run_files:
        if os.path.exists(file):
            df = pd.read_csv(file)
            run_data[file] = df
        else:
            print(f"Warning: {file} not found!")
            return

    # 1. Check that each condition appears exactly 5 times in each run
    for file, df in run_data.items():
        condition_counts = df["Condition"].value_counts()
        if not all(condition_counts == 5):
            print(f"❌ {file} does not have exactly 5 of each condition!")
        else:
            print(f"✅ {file} has 5 of each condition.")

    # 2. Check that the average trial duration is 5.0
    for file, df in run_data.items():
        if "Trial Duration" in df.columns:
            avg_jitter = df["Trial Duration"].mean()
            if round(avg_jitter, 2) != 5.0:
                print(f"❌ {file} does not have an average trial duration of 5.0 (Actual: {avg_jitter})")
            else:
                print(f"✅ {file} has an average trial duration of 5.0.")
        else:
            print(f"⚠️ {file} does not contain a 'trial duration' column.")

    # 3. Check for word overlap between runs with the same Run_Type
    word_run_tracker = defaultdict(set)  # Dictionary to track {word: {run_types where it appears}}

    for file, df in run_data.items():
        if "Input Modality" in df.columns:
            for _, row in df.iterrows():
                word_run_tracker[(row["Word"], row["Input Modality"])].add(file)
        else:
            print(f"⚠️ {file} does not contain a 'Input Modality' column.")
            
    # 4 Check that Male/Female distribution is even 
    for file, df in run_data.items():
        if "Audio File" in df.columns:
            df["Audio File"] = df["Audio File"].astype(str)  # Convert to string
            male_count = df[df["Audio File"].str.contains("Male", na=False)].shape[0]
            female_count = df[df["Audio File"].str.contains("Female", na=False)].shape[0]
            if male_count != female_count:
                print(f"❌ {file} does not have an even Male/Female distribution (Male: {male_count}, Female: {female_count})")
            else:
                print(f"✅ {file} has an even Male/Female distribution.")
        else:
            print(f"⚠️ {file} does not contain an 'Audio File' column.")

    # Find words that appear in multiple runs with the same Input Modality
    overlapping_words = {word: runs for word, runs in word_run_tracker.items() if len(runs) > 1}

    if overlapping_words:
        print("❌ Overlapping words found in multiple runs with the same Input Modality:")
        for (word, run_type), runs in overlapping_words.items():
            print(f"    - Word '{word}' (Input Modality: {run_type}) appears in {runs}")
    else:
        print("✅ No overlapping words between runs with the same Input Modality!")
        
        
        
# Test
# File paths
input_csv = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Paradigm\Input_Data\English\en_paradigm.csv"
output_dir = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Paradigm\Stimuli\Subject_Sampled_Stimuli"
stimuli_path= r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\English\English_Stimuli.csv"


SUBJECT_NAME = 'Christophe_Test'
create_subject_csvs(input_csv, output_dir, stimuli_path, SUBJECT_NAME)
validate_runs(SUBJECT_NAME)

