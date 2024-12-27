import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the csv data into a dataframe

csv_file_path = r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/english_test_data.csv'
df_stimuli = pd.read_csv(csv_file_path)

# Filter based on conditions

RLLC_df = df_stimuli.query('Lexicality == "real" and Size == "long" and Frequency == "low" and Morphology == "complex"')
RLLS_df = df_stimuli.query('Lexicality == "real" and Size == "long" and Frequency == "low" and Morphology == "simple"')
RSLC_df = df_stimuli.query('Lexicality == "real" and Size == "short" and Frequency == "low" and Morphology == "complex"')
RSHS_df = df_stimuli.query('Lexicality == "real" and Size == "short" and Frequency == "high" and Morphology == "simple"')
RLHS_df = df_stimuli.query('Lexicality == "real" and Size == "long" and Frequency == "high" and Morphology == "simple"')
RSLS_df = df_stimuli.query('Lexicality == "real" and Size == "short" and Frequency == "low" and Morphology == "simple"')
RLHC_df = df_stimuli.query('Lexicality == "real" and Size == "long" and Frequency == "high" and Morphology == "complex"')
RSHC_df = df_stimuli.query('Lexicality == "real" and Size == "short" and Frequency == "high" and Morphology == "complex"')
PLC_df = df_stimuli.query('Lexicality == "pseudo" and Size == "long" and Morphology == "complex"')
PLS_df = df_stimuli.query('Lexicality == "pseudo" and Size == "long" and Morphology == "simple"')
PSS_df = df_stimuli.query('Lexicality == "pseudo" and Size == "short" and Morphology == "simple"')
PSC_df = df_stimuli.query('Lexicality == "pseudo" and Size == "short" and Morphology == "complex"')

# Take a random sample of 15 words from each condition

sample_RLLC_df = RLLC_df.sample(n=15, random_state=42)
sample_RLLS_df = RLLS_df.sample(n=15, random_state=42)
sample_RSLC_df = RSLC_df.sample(n=15, random_state=42)
sample_RSHS_df = RSHS_df.sample(n=15, random_state=42)
sample_RLHS_df = RLHS_df.sample(n=15, random_state=42)
sample_RSLS_df = RSLS_df.sample(n=15, random_state=42)
sample_RLHC_df = RLHC_df.sample(n=15, random_state=42)
sample_RSHC_df = RSHC_df.sample(n=15, random_state=42)
sample_PLC_df = PLC_df.sample(n=15, random_state=42)
sample_PLS_df = PLS_df.sample(n=15, random_state=42)
sample_PSS_df = PSS_df.sample(n=15, random_state=42)
sample_PSC_df = PSC_df.sample(n=15, random_state=42)


# Creata a column on sample dataframes with explicit condition for plot

sample_RLLC_df['Condition'] = 'RLLC'
sample_RLLS_df['Condition'] = 'RLLS'
sample_RSLC_df['Condition'] = 'RSLC'
sample_RSHS_df['Condition'] = 'RSHS'
sample_RLHS_df['Condition'] = 'RLHS'
sample_RSLS_df['Condition'] = 'RSLS'
sample_RLHC_df['Condition'] = 'RLHC'
sample_RSHC_df['Condition'] = 'RSHC'
sample_PLC_df['Condition'] = 'PLC'
sample_PLS_df['Condition'] = 'PLS'
sample_PSS_df['Condition'] = 'PSS'
sample_PSC_df['Condition'] = 'PSC'


# Replace Words with overlapping/outlying frequencies

# Update all other columns except 'Phonemes'
sample_RSHS_df.loc[sample_RSHS_df['Word'] == 'govern', ['Word', 'Length', 'Zipf Frequency', 'Part of Speech']] = ['guitar', 6, 4.48, 'NOUN']
sample_RSHS_df.loc[sample_RSHS_df['Word'] == 'drone', ['Word', 'Length', 'Zipf Frequency', 'Part of Speech']] = ['truck', 5, 4.64, 'NOUN']
sample_RSHS_df.loc[sample_RSHS_df['Word'] == 'hack', ['Word', 'Length', 'Zipf Frequency', 'Part of Speech']] = ['tank', 4, 4.57, 'NOUN']
sample_RSHS_df.loc[sample_RSHS_df['Word'] == 'school', ['Word', 'Length', 'Zipf Frequency', 'Part of Speech']] = ['jersey', 6, 4.66, 'NOUN']


sample_RSLS_df.loc[sample_RSLS_df['Word'] == 'bullet', ['Word', 'Length', 'Zipf Frequency', 'Part of Speech']] = ['trifle', 6, 2.93, 'VERB']
sample_RSLS_df.loc[sample_RSLS_df['Word'] == 'castle', ['Word', 'Length', 'Zipf Frequency', 'Part of Speech']] = ['writhe', 6, 2.24, 'VERB']

sample_RLLS_df.loc[sample_RLLS_df['Word'] == 'stimulus', ['Word', 'Length', 'Zipf Frequency', 'Part of Speech']] = ['trombone', 8, 2.97, 'NOUN']
sample_RLLS_df.loc[sample_RLLS_df['Word'] == 'threshold', ['Word', 'Length', 'Zipf Frequency', 'Part of Speech']] = ['versatile', 9, 3.66, 'ADJ']
sample_RLLS_df.loc[sample_RLLS_df['Word'] == 'catalogue', ['Word', 'Length', 'Zipf Frequency', 'Part of Speech']] = ['chameleon', 9, 3.10, 'NOUN']
sample_RLLS_df.loc[sample_RLLS_df['Word'] == 'neighbour', ['Word', 'Length', 'Zipf Frequency', 'Part of Speech']] = ['boomerang', 9, 3.06, 'NOUN'] #to eliminate errors in cultural differences of spelling

sample_RSHC_df.loc[sample_RSHC_df['Word'] == 'into', ['Word', 'Length', 'Zipf Frequency', 'Part of Speech']] = ['worn', 4, 4.26, 'VERB']
sample_RSHC_df.loc[sample_RSHC_df['Word'] == 'nary', ['Word', 'Length', 'Zipf Frequency', 'Part of Speech']] = ['unit', 4, 4.96, 'NOUN']
sample_RSHC_df.loc[sample_RSHC_df['Word'] == 'wounds', ['Word', 'Length', 'Zipf Frequency', 'Part of Speech']] = ['writes', 6, 4.36, 'VERB']
sample_RSHC_df.loc[sample_RSHC_df['Word'] == 'flags', ['Word', 'Length', 'Zipf Frequency', 'Part of Speech']] = ['enjoy', 5, 5.09, 'VERB']
sample_RSHC_df.loc[sample_RSHC_df['Word'] == 'hurts', ['Word', 'Length', 'Zipf Frequency', 'Part of Speech']] = ['actor', 5, 4.65, 'NOUN']
sample_RSHC_df.loc[sample_RSHC_df['Word'] == 'rings', ['Word', 'Length', 'Zipf Frequency', 'Part of Speech']] = ['daily', 5, 5.07, 'ADV']
sample_RSHC_df.loc[sample_RSHC_df['Word'] == 'bloody', ['Word', 'Length', 'Zipf Frequency', 'Part of Speech']] = ['across', 6, 5.25, 'ADP']
sample_RSHC_df.loc[sample_RSHC_df['Word'] == 'deaths', ['Word', 'Length', 'Zipf Frequency', 'Part of Speech']] = ['hearts', 6, 4.44, 'NOUN']

sample_RLLC_df.loc[sample_RLLC_df['Word'] == 'wishfully', ['Word', 'Length', 'Zipf Frequency', 'Part of Speech']] = ['womanizer', 9, 2.61, 'NOUN']

# For Phonemes, assign as a proper list (not sure how to do otherwise)
sample_RSHS_df.at[sample_RSHS_df.index[sample_RSHS_df['Word'] == 'guitar'][0], 'Phonemes'] = ['G', 'IH0', 'T', 'AA1', 'R']
sample_RSHS_df.at[sample_RSHS_df.index[sample_RSHS_df['Word'] == 'truck'][0], 'Phonemes'] = ['T', 'R', 'AH1', 'K']
sample_RSHS_df.at[sample_RSHS_df.index[sample_RSHS_df['Word'] == 'tank'][0], 'Phonemes'] = ['T', 'AE1', 'NG', 'K']
sample_RSHS_df.at[sample_RSHS_df.index[sample_RSHS_df['Word'] == 'jersey'][0], 'Phonemes'] = ['JH', 'ER1', 'Z', 'IY0']



sample_RSLS_df.at[sample_RSLS_df.index[sample_RSLS_df['Word'] == 'trifle'][0], 'Phonemes'] = ['T', 'R', 'AY1', 'F', 'AH0', 'L']
sample_RSLS_df.at[sample_RSLS_df.index[sample_RSLS_df['Word'] == 'writhe'][0], 'Phonemes'] =  ['R', 'IH1', 'TH']

sample_RLLS_df.at[sample_RLLS_df.index[sample_RLLS_df['Word'] == 'trombone'][0], 'Phonemes'] =  ['T', 'R', 'AA0', 'M', 'B', 'OW1', 'N']
sample_RLLS_df.at[sample_RLLS_df.index[sample_RLLS_df['Word'] == 'versatile'][0], 'Phonemes'] =  ['V', 'ER1', 'S', 'AH0', 'T', 'AH0', 'L']
sample_RLLS_df.at[sample_RLLS_df.index[sample_RLLS_df['Word'] == 'chameleon'][0], 'Phonemes'] = ['CH', 'AH0', 'M', 'EH1', 'L', 'IY0', 'AH0', 'N']
sample_RLLS_df.at[sample_RLLS_df.index[sample_RLLS_df['Word'] == 'boomerang'][0], 'Phonemes'] = ['B', 'UW1', 'M', 'ER0', 'AE2', 'NG']

sample_RSHC_df.at[sample_RSHC_df.index[sample_RSHC_df['Word'] == 'worn'][0], 'Phonemes'] = ['W', 'AO1', 'R', 'N']
sample_RSHC_df.at[sample_RSHC_df.index[sample_RSHC_df['Word'] == 'unit'][0], 'Phonemes'] = ['Y', 'UW1', 'N', 'AH0', 'T']
sample_RSHC_df.at[sample_RSHC_df.index[sample_RSHC_df['Word'] == 'writes'][0], 'Phonemes'] = ['R', 'AY1', 'T', 'S']
sample_RSHC_df.at[sample_RSHC_df.index[sample_RSHC_df['Word'] == 'enjoy'][0], 'Phonemes'] = ['EH0', 'N', 'JH', 'OY1']
sample_RSHC_df.at[sample_RSHC_df.index[sample_RSHC_df['Word'] == 'actor'][0], 'Phonemes'] = ['AE1', 'K', 'T', 'ER0']
sample_RSHC_df.at[sample_RSHC_df.index[sample_RSHC_df['Word'] == 'daily'][0], 'Phonemes'] = ['D', 'EY1', 'L', 'IY0']
sample_RSHC_df.at[sample_RSHC_df.index[sample_RSHC_df['Word'] == 'across'][0], 'Phonemes'] = ['AH0', 'K', 'R', 'AO1', 'S']
sample_RSHC_df.at[sample_RSHC_df.index[sample_RSHC_df['Word'] == 'hearts'][0], 'Phonemes'] = ['HH', 'AA1', 'R', 'T', 'S']

sample_RLLC_df.at[sample_RLLC_df.index[sample_RLLC_df['Word'] == 'womanizer'][0], 'Phonemes'] = ['W', 'UH1', 'M', 'AH0', 'N', 'AY2', 'Z', 'ER0']

'''
# Print the filtered DataFrame to find outliers

print(sample_RSLC_df[['Word','Zipf Frequency']])
print('\n')
print(RSLC_df[['Word', 'Zipf Frequency']])
print('\n')
print(RSLC_df)
'''

# Concatenate all sample dfs into a single df
all_samples_with_frequencies_df= pd.concat([sample_RLLC_df, sample_RLLS_df, sample_RSLC_df, sample_RSHS_df, sample_RLHS_df, sample_RSLS_df, sample_RLHC_df, sample_RSHC_df])

all_samples_with_frequencies_df.to_csv('C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/english_sample_stimuli.csv', index=False)




# Scatter Plot:

# Define custom color function
def get_custom_color(row):
    if row['Condition'] == 'RLLC' :
        return 'pink'
    elif row['Condition'] == 'RLLS' :
        return 'salmon'
    elif row['Condition'] == 'RLHC' :
        return 'crimson'
    elif row['Condition'] == 'RLHS' :
        return 'maroon'
    elif row['Condition'] == 'RSHS' :
        return 'deepskyblue'
    elif row['Condition'] == 'RSHC' :
        return 'indigo'
    elif row['Condition'] == 'RSLC' :
        return 'lightblue'
    elif row['Condition'] == 'RSLS' :
        return 'lightskyblue'

# Add a 'Custom Color' column
all_samples_with_frequencies_df['Custom Color'] = all_samples_with_frequencies_df.apply(get_custom_color, axis=1)

# Plot with scatterplot
scatter = sns.scatterplot(
    data=all_samples_with_frequencies_df,
    x="Length", 
    y="Zipf Frequency", 
    hue="Condition",  # For color legend
    style="Morphology",  # For shape legend
    style_order=['simple', 'complex'], 
    markers={'simple': 'o', 'complex': 'X'},  # Compatible filled markers
    palette=list(all_samples_with_frequencies_df['Custom Color'].unique()),  # Convert to list
    legend='brief'  # Ensures legend displays
)


plt.title('Comparison of Length and Frequency Across 12 Conditions', y=1.06)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title='Legend')
plt.show()

# remove color column from df
del all_samples_with_frequencies_df['Custom Color']
