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

# Function to merge additional columns from French_Stimuli.csv
def merge_additional_columns(df, stimuli_path):
    # Read the French_Stimuli.csv file
    stimuli_df = pd.read_csv(stimuli_path)

    # Select the required columns
    columns_to_merge = ['Word', 'Zipf Lemma Frequency', 'Lemma', 'Zipf Frequency','Morphology', 'Length', 'Lexicality']
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
    
    # Reorder columns to place Condition to the left of 
    columns = df.columns.tolist()
    condition_index = columns.index('Condition')
    input_modality_index = columns.index('Wordlength')
    columns.insert(input_modality_index, columns.pop(condition_index))
    df = df[columns]
    
    return df

# Define function to assign jitter durations based on an even distribtion

def assign_jitter_durations(n_stimuli, mean_soa, step=0.5, n_durations=5):
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

    # Store dataframes for the 8 runs
    run_dataframes = []

    # Create dictionaries to store lists and dataframes for each run type
    run_lists = {'vs': [], 'as': [], 'vt': [], 'at': []}
    run_dfs = {'vs': None, 'as': None, 'vt': None, 'at': None}

    for i in range(4):  # We need 4 mutually exclusive sets
        for condition in conditions:
            # Select 4 words for this batch
            condition_words = df[df["Condition"] == condition].copy()

            if len(condition_words) < 20-4*i:
                raise ValueError(f"Not enough words in condition {condition} for run {i+1}.")

            # Select 4 words per condition, with two being from one Wordlength and two from another
            lengths = condition_words['Wordlength'].unique()
            if len(lengths) != 2:
                raise ValueError(f"Condition {condition} does not have exactly two unique word lengths.")

            length1_words = condition_words[condition_words['Wordlength'] == lengths[0]]
            length2_words = condition_words[condition_words['Wordlength'] == lengths[1]]

            if len(length1_words) < 2 or len(length2_words) < 2:
                raise ValueError(f"Not enough words in condition {condition} for one of the lengths.")

            selected_words = pd.concat([length1_words.iloc[:2], length2_words.iloc[:2]])
            condition_words = condition_words.drop(selected_words.index)

            # Remove the selected words from the main dataframe to avoid reuse
            df = df.drop(selected_words.index)

            # Append selected words to the appropriate list
            if i == 0:
                run_lists['vs'].append(selected_words)
            elif i == 1:
                run_lists['as'].append(selected_words)
            elif i == 2:
                run_lists['vt'].append(selected_words)
            elif i == 3:
                run_lists['at'].append(selected_words)

    # Concatenate lists into dataframes
    for run_type in run_lists:
        run_dfs[run_type] = pd.concat(run_lists[run_type], ignore_index=True)

    # Shuffle the entire DataFrame to mix conditions & words
    for run_type in run_dfs:
        run_dfs[run_type] = run_dfs[run_type].sample(frac=1, random_state=None).reset_index(drop=True)

    # Assign trial durations (Jitter Duration + 0.5 fixation) IMPORTANT TO SUBTRACT IN SCRIPT!!!
    n_stimuli = len(run_dfs['vs'])  # Same length for all trials
    run_dfs['vs']["Trial Duration"] = assign_jitter_durations(n_stimuli, mean_soa=5)
    run_dfs['as']["Trial Duration"] = assign_jitter_durations(n_stimuli, mean_soa=5)
    run_dfs['vt']["Trial Duration"] = assign_jitter_durations(n_stimuli, mean_soa=10)
    run_dfs['at']["Trial Duration"] = assign_jitter_durations(n_stimuli, mean_soa=10)

    # Assign run type
    run_dfs['vs']["Input Modality"] = "Visual"
    run_dfs['vs']["Output Modality"] = "Speech"

    run_dfs['as']["Input Modality"] = "Audio"
    run_dfs['as']["Output Modality"] = "Speech"

    run_dfs['vt']["Input Modality"] = "Visual"
    run_dfs['vt']["Output Modality"] = "Type"

    run_dfs['at']["Input Modality"] = "Audio"
    run_dfs['at']["Output Modality"] = "Type"
    
    # Add additional information from original csv
    # for run_type in run_dfs:
    #     run_dfs[run_type] = merge_additional_columns(run_dfs[run_type], stimuli_path)

    # Adjust audio to 50/50 Male/Female distribution
    for run_type in run_dfs:
        run_dfs[run_type] = assign_audio_gender(run_dfs[run_type], len(run_dfs[run_type]))

    # Append them to run_dataframes
    run_dataframes.extend(run_dfs.values())

    
    # Randomize the run indices (so runs aren't always in a set order)
    run_indices = np.random.permutation(4) + 1  # Generate 1-4 in random order

    # Save each dataframe with assigned run number
    for idx, run_df in enumerate(run_dataframes):
        run_filename = f"{subject_name}_Run_{run_indices[idx]}.csv"
        output_file = os.path.join(output_dir, run_filename)
        run_df.to_csv(output_file, index=False)
        print(f"Saved {run_filename}")

    
# Validate to ensure no mistakes (sanity check)
def validate_runs(subject_name, base_dir):
    run_files = [os.path.join(base_dir, f"{subject_name}_Run_{i}.csv") for i in range(1, 5)]
    run_data = {}

    # Load all runs
    for file in run_files:
        if os.path.exists(file):
            df = pd.read_csv(file)
            run_data[file] = df
        else:
            print(f"Warning: {file} not found!")
            return

    # 1. Check that each condition appears exactly 4 times in each run
    for file, df in run_data.items():
        condition_counts = df["Condition"].value_counts()
        if not all(condition_counts == 4):
            print(f"❌ {file} does not have exactly 4 of each condition!")
        else:
            print(f"✅ {file} has 4 of each condition.")

    # 2. Check that the average trial duration is 5.0 for Speech Output Modality and 10.0 for Type Output Modality
    for file, df in run_data.items():
        if "Trial Duration" in df.columns and "Output Modality" in df.columns:
            output_modality = df["Output Modality"].iloc[0]
            if output_modality == 'Speech':
                expected_duration = 5.0
            elif output_modality == 'Type':
                expected_duration = 10.0
            else:
                print(f"⚠️ {file} has an unexpected Output Modality: {output_modality}")
                continue

            avg_jitter = df["Trial Duration"].mean()
            if round(avg_jitter, 2) != expected_duration:
                print(f"❌ {file} does not have an average trial duration of {expected_duration} for {output_modality} (Actual: {avg_jitter})")
            else:
                print(f"✅ {file} has an average trial duration of {expected_duration} for {output_modality}.")
        else:
            print(f"⚠️ {file} does not contain 'Trial Duration' or 'Output Modality' columns.")

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
input_csv = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Paradigm\Input_Data\French\fr_paradigm.csv"
output_dir = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Paradigm\Input_Data\French\Subject_Sampled_Stimuli"
stimuli_path= r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\French\French_Stimuli.csv"


SUBJECT_NAME = 'Pilot' # Enter subject name
create_subject_csvs(input_csv, output_dir, stimuli_path, SUBJECT_NAME)
validate_runs(SUBJECT_NAME, base_dir=output_dir)

