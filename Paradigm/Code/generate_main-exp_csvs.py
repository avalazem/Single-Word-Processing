import pandas as pd
import random
import os
import numpy as np
from collections import defaultdict

# Function to generate a 50/50 gender list
def generate_gender_list(n_entries):
    half = n_entries // 2
    gender_list = ['M'] * half + ['F'] * half
    if n_entries % 2 == 1:
        gender_list.append(random.choice(['M', 'F']))
        print("Warning: Odd Number of Stimuli - won't be 50/50!")
    random.shuffle(gender_list)
    return gender_list

# Function to merge additional columns from French_Stimuli.csv
def merge_additional_columns(df, stimuli_path):
    stimuli_df = pd.read_csv(stimuli_path)
    columns_to_merge = ['Word', 'Zipf Lemma Frequency', 'Lemma', 'Zipf Frequency', 'Morphology', 'Length', 'Lexicality']
    stimuli_df = stimuli_df[columns_to_merge]
    merged_df = pd.merge(df, stimuli_df, on='Word', how='left')
    condition_index = merged_df.columns.get_loc('Word')
    new_order = merged_df.columns.tolist()
    for col in columns_to_merge[1:]:
        new_order.insert(condition_index + 1, new_order.pop(new_order.index(col)))
    merged_df = merged_df[new_order]
    merged_df.rename(columns={'Morphology': 'Morphological Complexity'}, inplace=True)
    return merged_df

# Function to update run type and assign audio files based on gender
def assign_audio_gender(df, n_stimuli):
    gender_list = generate_gender_list(n_stimuli)
    df['Audio File'] = [row.Audio_Male if gender == 'M' else row.Audio_Female for row, gender in zip(df.itertuples(), gender_list)]
    df.loc[df['Input Modality'] != 'Audio', 'Audio File'] = None
    df.drop(columns=['Audio_Male', 'Audio_Female'], inplace=True)
    columns = df.columns.tolist()
    audio_index = columns.index('Audio File')
    input_modality_index = columns.index('Input Modality')
    columns.insert(input_modality_index, columns.pop(audio_index))
    df = df[columns]
    columns = df.columns.tolist()
    condition_index = columns.index('Condition')
    input_modality_index = columns.index('Wordlength')
    columns.insert(input_modality_index, columns.pop(condition_index))
    df = df[columns]
    return df

# Define function to assign jitter durations based on an even distribution
def assign_jitter_durations(n_stimuli, mean_soa, step=0.5, n_durations=5):
    durations = [mean_soa - step * (i - (n_durations - 1) / 2) for i in range(n_durations)]
    base_repeats = n_stimuli // n_durations
    remainder = n_stimuli % n_durations
    assigned_durations = durations * base_repeats + [mean_soa] * remainder
    np.random.shuffle(assigned_durations)
    assert np.isclose(sum(assigned_durations), n_stimuli * mean_soa, atol=1e-6), "Sum of durations does not match the total required duration"
    return assigned_durations

def create_subject_csvs(input_csv, output_dir, stimuli_path, subject_name):
    df = pd.read_csv(input_csv)
    required_columns = {"Word", "Condition", "Audio_Male", "Audio_Female", "Wordlength"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"CSV must contain the columns: {required_columns}")

    
    # Define run modalities
    run_modalities = [
        ['vs', 'as', 'vt', 'at'],  # First 3 runs
        ['vs', 'as', 'vw', 'aw']   # Next 3 runs
    ]
    n_runs = 6
    reps_per_condition = 1

    # Prepare data structures
    run_dataframes = []

    for run_idx in range(n_runs):
        run_blocks = []
        run_modality = run_modalities[run_idx % len(run_modalities)]
        random.shuffle(run_modality)
        run_df = df.copy()  # Create a fresh copy of the dataframe for each run

        for modality in run_modality:
            conditions = df["Condition"].unique()
            if len(conditions) != 12:
                    raise ValueError("There must be exactly 12 conditions in the input CSV.")
            random.shuffle(conditions)
            for condition in conditions:
                # Filter stimuli for the current condition
                condition_words = run_df[run_df["Condition"] == condition].copy()
                if len(condition_words) < reps_per_condition:
                    raise ValueError(f"Not enough stimuli for condition {condition} and modality {modality} in run {run_idx + 1}")

                # Randomly sample stimuli for the current modality and condition
                selected_words = condition_words.sample(n=reps_per_condition, random_state=None)
                run_df = run_df.drop(selected_words.index)
                selected_words["Modality"] = modality
                run_blocks.append(selected_words)

        # Add blocks to the run dataframe
        run_df = pd.concat(run_blocks, ignore_index=True)

        # Assign input/output modalities and trial durations
        for modality in run_df["Modality"].unique():
            input_modality = "Visual" if modality[0] == 'v' else "Audio"
            output_modality = {
                's': "Speech",
                'w': "Write",
                't': "Type"
            }[modality[1]]

            run_df.loc[run_df["Modality"] == modality, "Input Modality"] = input_modality
            run_df.loc[run_df["Modality"] == modality, "Output Modality"] = output_modality

            # Assign trial durations at the block level
            block_df = run_df[run_df["Modality"] == modality]
            n_stimuli = len(block_df)
            mean_soa = 5 if output_modality == "Speech" else 10
            run_df.loc[block_df.index, "Trial Duration"] = assign_jitter_durations(n_stimuli, mean_soa=mean_soa)

        run_df = assign_audio_gender(run_df, len(run_df))

        # Drop superfluous Modality column
        run_df.drop(columns=["Modality"], inplace=True)
        
        # Add run to the runs dataframe
        run_dataframes.append(run_df)

    # Save runs to CSV files
    for idx, run_df in enumerate(run_dataframes):
        run_filename = f"{subject_name}_run_{idx + 1}.csv"
        output_file = os.path.join(output_dir, run_filename)
        run_df.to_csv(output_file, index=False)
        print(f"Saved {run_filename}")

def validate_runs(subject_name, base_dir):
    run_files = [os.path.join(base_dir, f"{subject_name}_run_{i}.csv") for i in range(1, 7)]
    run_data = {}

    for file in run_files:
        if os.path.exists(file):
            df = pd.read_csv(file)
            run_data[file] = df
        else:
            print(f"Warning: {file} not found!")
            return

    for file, df in run_data.items():
        condition_counts = df["Condition"].value_counts()
        if not all(condition_counts == 4):
            print(f"❌ {file} does not have exactly 4 of each condition!")
        else:
            print(f"✅ {file} has 4 of each condition.")

    for file, df in run_data.items():
        if "Trial Duration" in df.columns:
            # Define expected trial mean based on output modality
            expected_trial_mean = 7.5
            # Calculate the average trial duration  
            avg_jitter = df["Trial Duration"].mean()
            if round(avg_jitter, 2) != expected_trial_mean:
                print(f"❌ {file} does not have an average trial duration of 7.5 (Actual: {avg_jitter})")
            else:
                print(f"✅ {file} has an average trial duration of 7.5")
        else:
            print(f"⚠️ {file} does not contain a 'trial duration' column.")

    word_run_tracker = defaultdict(set)

    for file, df in run_data.items():
        if "Input Modality" in df.columns:
            for _, row in df.iterrows():
                word_run_tracker[(row["Word"], row["Input Modality"])].add(file)
        else:
            print(f"⚠️ {file} does not contain a 'Input Modality' column.")
            
    for file, df in run_data.items():
        if "Audio File" in df.columns:
            df["Audio File"] = df["Audio File"].astype(str)
            male_count = df[df["Audio File"].str.contains("Male", na=False)].shape[0]
            female_count = df[df["Audio File"].str.contains("Female", na=False)].shape[0]
            if male_count != female_count:
                print(f"❌ {file} does not have an even Male/Female distribution (Male: {male_count}, Female: {female_count})")
            else:
                print(f"✅ {file} has an even Male/Female distribution.")
        else:
            print(f"⚠️ {file} does not contain an 'Audio File' column.")

    for file, df in run_data.items():
        overlapping_words = df[df.duplicated(subset=["Word", "Input Modality"], keep=False)]
        if not overlapping_words.empty:
            print(f"❌ Overlapping words found within {file}:")
            for _, row in overlapping_words.iterrows():
                print(f"    - Word '{row['Word']}' with Input Modality '{row['Input Modality']}'")
        else:
            print(f"✅ No overlapping words within {file}!")






# Test
input_csv = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Paradigm\Input_Data\French\fr_paradigm.csv"
output_dir = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Paradigm\Input_Data\French\Run_Csvs"
stimuli_path= r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\French\French_Stimuli.csv"

SUBJECT_NAME = 'sub1'
create_subject_csvs(input_csv, output_dir, stimuli_path, SUBJECT_NAME)
#validate_runs(SUBJECT_NAME, base_dir=output_dir)