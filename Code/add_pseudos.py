import pandas as pd

# Load the CSV files
stimuli_df = pd.read_csv('C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/English Data/english_test_data.csv')
my_stimuli_df = pd.read_csv(r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/English Data/english_sample_stimuli_withlemmas.csv')

# Filter the DataFrame to only include rows with Lexicality "pseudo"
pseudo_df = stimuli_df[stimuli_df['Lexicality'] == 'pseudo']

# List to hold the samples
sampled_rows = []

# Group by 'Length' and 'Morphology', then sample 5 rows per group
for (length, morphology), group in pseudo_df.groupby(['Length', 'Morphology']):
    if len(group) >= 5:  # Ensure there are enough rows to sample
        sampled_rows.append(group.sample(n=5, random_state=42))

# Concatenate all the sampled rows back into a single DataFrame
sampled_df = pd.concat(sampled_rows)

# Ensure the columns are in the same order as the original dataframe
sampled_df = sampled_df[stimuli_df.columns]

# Reset index to flatten the DataFrame and drop the index column
sampled_df = sampled_df.reset_index(drop=True)

# Remove 'Unnamed: 0' column if it exists in either DataFrame
if 'Unnamed: 0' in sampled_df.columns:
    sampled_df = sampled_df.drop(columns=['Unnamed: 0'])

if 'Unnamed: 0' in my_stimuli_df.columns:
    my_stimuli_df = my_stimuli_df.drop(columns=['Unnamed: 0'])


# Filter into separate dataframes (probably a better way to do this)

PLC_df =  sampled_df.query('Lexicality == "pseudo" and Size == "long" and Morphology == "complex"')
PLS_df =  sampled_df.query('Lexicality == "pseudo" and Size == "long" and Morphology == "simple"')
PSS_df =  sampled_df.query('Lexicality == "pseudo" and Size == "short" and Morphology == "simple"')
PSC_df =  sampled_df.query('Lexicality == "pseudo" and Size == "short" and Morphology == "complex"')

# Add Conditions
PLC_df['Condition'] = 'PLC'
PLS_df['Condition'] = 'PLS'
PSS_df['Condition'] = 'PSS'
PSC_df['Condition'] = 'PSC'


# Combine the dataframes
combined_df = pd.concat([my_stimuli_df, PLC_df, PLS_df, PSS_df, PSC_df])

# Write the combined dataframe to a new CSV, without the index column
#combined_df.to_csv(r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/English Data/english_sample_stimuli_addlemmas_addpseudos.csv', index=False)
