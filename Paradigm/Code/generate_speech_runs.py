import pandas as pd
import random
import os
import numpy as np
from collections import defaultdict


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


# File paths
input_csv = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Paradigm\Stimuli\en_paradigm.csv"
output_dir = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Paradigm\Stimuli\Subject_Sampled_Stimuli"

def create_subject_csvs(input_csv, output_dir, subject_name):
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

        # Assign jitter durations
        n_stimuli = len(ws_df) # Same length for both ws and as
        ws_df["Jitter_Duration"] = assign_jitter_durations(n_stimuli)
        as_df["Jitter_Duration"] = assign_jitter_durations(n_stimuli)

        # Assign run type
        ws_df["Run_Type"] = "ws"
        as_df["Run_Type"] = "as"

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

    # 2. Check that the average jitter_duration is 5.0
    for file, df in run_data.items():
        if "Jitter_Duration" in df.columns:
            avg_jitter = df["Jitter_Duration"].mean()
            if round(avg_jitter, 2) != 5.0:
                print(f"❌ {file} does not have an average jitter_duration of 5.0 (Actual: {avg_jitter})")
            else:
                print(f"✅ {file} has an average jitter_duration of 5.0.")
        else:
            print(f"⚠️ {file} does not contain a 'jitter_duration' column.")

    # 3. Check for word overlap between runs with the same Run_Type
    word_run_tracker = defaultdict(set)  # Dictionary to track {word: {run_types where it appears}}

    for file, df in run_data.items():
        if "Run_Type" in df.columns:
            for _, row in df.iterrows():
                word_run_tracker[(row["Word"], row["Run_Type"])].add(file)
        else:
            print(f"⚠️ {file} does not contain a 'Run_Type' column.")

    # Find words that appear in multiple runs with the same Run_Type
    overlapping_words = {word: runs for word, runs in word_run_tracker.items() if len(runs) > 1}

    if overlapping_words:
        print("❌ Overlapping words found in multiple runs with the same Run_Type:")
        for (word, run_type), runs in overlapping_words.items():
            print(f"    - Word '{word}' (Run_Type: {run_type}) appears in {runs}")
    else:
        print("✅ No overlapping words between runs with the same Run_Type!")
        
        
        
# Test
#create_subject_csvs(input_csv, output_dir, "Test_Subject_Two")
validate_runs("Test_Subject_Two")
