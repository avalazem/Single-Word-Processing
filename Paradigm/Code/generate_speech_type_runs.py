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
    required_columns = {"Word", "Condition", "Audio_Male", "Audio_Female"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"CSV must contain the columns: {required_columns}")

    conditions = df["Condition"].unique()
    run_dataframes = []
    run_lists = {'vs_1': [], 'as_1': [], 'vt': [], 'at': [], 'vs_2': [], 'as_2': [], 'vw': [], 'aw': []}
    run_dfs = {'vs_1': None, 'as_1': None, 'vt': None, 'at': None, 'vs_2': None, 'as_2': None, 'vw': None, 'aw': None}

    n_runs = 8 # Define # runs
    n_conditions = 2 # Define # conditions
    for i in range(n_runs):  # We need 8 mutually exclusive sets
        for condition in conditions:
            # Take words from the specified condition and shuffle them
            condition_words = df[df["Condition"] == condition].copy()
            if len(condition_words) < 20 - n_conditions * i:
                raise ValueError(f"Not enough words in condition {condition} for run {i + 1}.")
            lengths = condition_words['Wordlength'].unique()
            if len(lengths) != n_conditions:
                raise ValueError(f"Condition {condition} does not have exactly two unique word lengths.")
            length1_words = condition_words[condition_words['Wordlength'] == lengths[0]]
            length2_words = condition_words[condition_words['Wordlength'] == lengths[1]]
            if len(length1_words) < (n_conditions/2) or len(length2_words) < (n_conditions/2):
                raise ValueError(f"Not enough words in condition {condition} for one of the lengths.")
            selected_words = pd.concat([length1_words.sample(n=1, random_state=None), length2_words.sample(n=1, random_state=None)])
            condition_words = condition_words.drop(selected_words.index)
            df = df.drop(selected_words.index)
            if i == 0:
                run_lists['vs_1'].append(selected_words)
            elif i == 1:
                run_lists['as_1'].append(selected_words)
            elif i == 2:
                run_lists['vt'].append(selected_words)
            elif i == 3:
                run_lists['at'].append(selected_words)
            elif i == 4:
                run_lists['vs_2'].append(selected_words)
            elif i == 5:
                run_lists['as_2'].append(selected_words)
            elif i == 6:
                run_lists['vw'].append(selected_words)
            elif i == 7:
                run_lists['aw'].append(selected_words)
            

    for run_type in run_lists:
        run_dfs[run_type] = pd.concat(run_lists[run_type], ignore_index=True)

    for run_type in run_dfs:
        run_dfs[run_type] = run_dfs[run_type].sample(frac=1, random_state=None).reset_index(drop=True)


    for run_type in run_dfs:
        input_modality = "Visual" if run_type[0] == 'v' else "Audio"
        if run_type[1] == 's':
            output_modality = "Speech"
        elif run_type[1] == 'w':
            output_modality = "Write"
        elif run_type[1] == 't':
            output_modality = "Type"
        run_dfs[run_type]["Input Modality"] = input_modality
        run_dfs[run_type]["Output Modality"] = output_modality
    
    for run_type in run_dfs:
        n_stimuli = len(run_dfs[run_type])
        if run_dfs[run_type]["Output Modality"].iloc[0] == "Speech":
            mean_soa = 5
        else:
            mean_soa = 10
        run_dfs[run_type]["Trial Duration"] = assign_jitter_durations(n_stimuli, mean_soa=mean_soa)

    for run_type in run_dfs:
        run_dfs[run_type] = assign_audio_gender(run_dfs[run_type], len(run_dfs[run_type]))

    run_dataframes.extend(run_dfs.values())

    run_indices = np.random.permutation(n_runs) + 1  # Generate n_runs in random order

    for idx, run_df in enumerate(run_dataframes):
        run_filename = f"{subject_name}_Run_{run_indices[idx]}.csv"
        output_file = os.path.join(output_dir, run_filename)
        run_df.to_csv(output_file, index=False)
        print(f"Saved {run_filename}")

def validate_runs(subject_name, base_dir):
    run_files = [os.path.join(base_dir, f"{subject_name}_Run_{i}.csv") for i in range(1, 9)]
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
        if not all(condition_counts == 2):
            print(f"❌ {file} does not have exactly 2 of each condition!")
        else:
            print(f"✅ {file} has 2 of each condition.")

    for file, df in run_data.items():
        if "Trial Duration" in df.columns:
            # Define expected trial mean based on output modality
            if df["Output Modality"].iloc[0] == "Speech":
                expected_trial_mean = 5.0
            elif df["Output Modality"].iloc[0] == "Write":
                expected_trial_mean = 10.0
            elif df["Output Modality"].iloc[0] == "Type":
                expected_trial_mean = 10.0
            # Calculate the average trial duration  
            avg_jitter = df["Trial Duration"].mean()
            if round(avg_jitter, 2) != expected_trial_mean:
                print(f"❌ {file} does not have an average trial duration of 5.0 (Actual: {avg_jitter})")
            else:
                print(f"✅ {file} has an average trial duration of 5.0.")
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

    overlapping_words = {word: runs for word, runs in word_run_tracker.items() if len(runs) > 1}

    if overlapping_words:
        print("❌ Overlapping words found in multiple runs:")
        for word, runs in overlapping_words.items():
            print(f"    - Word '{word}' appears in {runs}")
    else:
        print("✅ No overlapping words between runs!")

# Test
input_csv = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Paradigm\Input_Data\French\fr_paradigm.csv"
output_dir = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Paradigm\Input_Data\French\Subject_Sampled_Stimuli"
stimuli_path= r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\French\French_Stimuli.csv"

SUBJECT_NAME = 'Pilot'
create_subject_csvs(input_csv, output_dir, stimuli_path, SUBJECT_NAME)
validate_runs(SUBJECT_NAME, base_dir=output_dir)