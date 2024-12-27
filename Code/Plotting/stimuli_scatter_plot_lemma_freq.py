import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

csv_path =r'C:\Users\ali_a\Desktop\Single Word Processing Stage\Single Word Processing\Data\English Data\English_Stimuli.csv'
stimuli_df = pd.read_csv(csv_path)

# Scatter Plot:

# Define custom color function
def get_custom_color(row):
    if row['Condition'] == 'RSLS' :
        return 'pink'
    elif row['Condition'] == 'RSLC' :
        return 'salmon'
    elif row['Condition'] == 'RLLS' :
        return 'crimson'
    elif row['Condition'] == 'RLLC' :
        return 'maroon'
    elif row['Condition'] == 'RSHS' :
        return 'lightblue'
    elif row['Condition'] == 'RSHC' :
        return 'lightskyblue'
    elif row['Condition'] == 'RLHS' :
        return 'deepskyblue'
    elif row['Condition'] == 'RLHC' :
        return 'indigo'

# Add a 'Custom Color' column
stimuli_df['Custom Color'] = stimuli_df.apply(get_custom_color, axis=1)

# Plot with scatterplot
scatter = sns.scatterplot(
    data=stimuli_df,
    x="Length", 
    y="Zipf Lemma Frequency", 
    hue="Condition",  # For color legend
    style="Morphology",  # For shape legend
    style_order=['simple', 'complex'], 
    markers={'simple': 'o', 'complex': 'X'},  # Compatible filled markers
    palette=list(stimuli_df['Custom Color'].unique()),  # Convert to list
    legend='brief'  # Ensures legend displays
)


plt.title('Comparison of Length and Lemma Frequency Across 8 Conditions', y=1.06)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title='Legend')
plt.show()

# remove color column from df
del stimuli_df['Custom Color']

# Quick Sanity Check
'''
# Filter the 'Length' column to ensure it's in the range of 4 to 10
stimuli_df_filtered = stimuli_df[stimuli_df['Length'].between(4, 10)]

# Group by 'Condition' and 'Length' and count occurrences
condition_length_counts = stimuli_df_filtered.groupby(['Condition', 'Length']).size().reset_index(name='Count')

# Display the counts for each combination of 'Condition' and 'Length'
print(condition_length_counts)
'''