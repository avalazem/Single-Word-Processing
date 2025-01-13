import pandas as pd
import random

import pandas as pd
import random

sample_set_path = r'C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\English\english_test_data.csv'
stimuli_being_used_path = r'C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\English\English_Stimuli.csv'
output_path = r'C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\Test_Stimuli_en.csv'

# Load the datasets
sample_set = pd.read_csv(sample_set_path)
stimuli_being_used = pd.read_csv(stimuli_being_used_path)

# Filter out words that are already being used
available_words = sample_set[~sample_set['Word'].isin(stimuli_being_used['Word'])]

# Ensure every condition is covered (12 total), with 6 being repeated
conditions = available_words['Condition'].unique()
selected_words = []

# Select one word for each condition
for condition in conditions:
    words_in_condition = available_words[available_words['Condition'] == condition]
    if not words_in_condition.empty:
        selected_words.append(words_in_condition.sample(1))

# Randomly select 6 conditions to repeat
repeated_conditions = random.choices(conditions, k=6)
for condition in repeated_conditions:
    words_in_condition = available_words[available_words['Condition'] == condition]
    if not words_in_condition.empty:
        selected_words.append(words_in_condition.sample(1))

# Combine the selected words into a single DataFrame
selected_words_df = pd.concat(selected_words).reset_index(drop=True)

# Select only the 'Word' and 'Condition' columns
selected_words_df = selected_words_df[['Word', 'Condition']]

# Save the selected words and their corresponding conditions to a new CSV file
selected_words_df.to_csv(output_path, index=False)

print(f"Selected words and their conditions have been saved to {output_path}")