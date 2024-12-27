import pandas as pd

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

stimuli_df = pd.read_csv(r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/English Data/english_sample_stimuli_pseudos.csv')

# Scatter Plot:

# Define custom color function
def get_custom_color(row):
    if row['Condition'] == 'PSC' :
        return 'lightskyblue'
    elif row['Condition'] == 'PSS' :
        return 'salmon'
    elif row['Condition'] == 'PLC' :
        return 'deepskyblue'
    elif row['Condition'] == 'PLS' :
        return 'maroon'

# Add a 'Custom Color' column
stimuli_df['Custom Color'] = stimuli_df.apply(get_custom_color, axis=1)

# Map Morphology to numerical values to graph
stimuli_df['Morphology_Num'] = stimuli_df['Morphology'].map({'simple': 0, 'complex': 1})

# Adjust y-axis labels to show Morphology names
plt.yticks([1, 0], labels=['simple', 'complex'])

# Plot with scatterplot
scatter = sns.scatterplot(
    data=stimuli_df,
    x="Length", 
    y="Morphology", 
    hue="Condition",  # For color legend
    style="Morphology",  # For shape legend
    style_order=['simple', 'complex'], 
    markers={'simple': 'o', 'complex': 'X'},  # Compatible filled markers
    palette=list(stimuli_df['Custom Color'].unique()),  # Convert to list
    legend='brief'  # Ensures legend displays
)


plt.title('Comparison of Length and Morphology Across 4 Conditions', y=1.06)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title='Legend')
plt.show()

# remove color column from df
del stimuli_df['Custom Color']