import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

csv_path = r'C:\Users\ali_a\Desktop\Single Word Processing Stage\Single Word Processing\Data\English Data\English_Stimuli.csv'
df_stimuli = pd.read_csv(csv_path)

# Filter data for Lexicality == 'real'
filtered_df = df_stimuli[df_stimuli['Lexicality'] == 'real']

# Group by Condition and Part of Speech and count occurrences
grouped_data = (
    filtered_df.groupby(['Condition', 'Part of Speech'])
    .size()
    .reset_index(name='Count')
)

# Pivot table for easier plotting
pivot_data = grouped_data.pivot(
    index='Condition', columns='Part of Speech', values='Count'
).fillna(0)

# Reset index for easier plotting
pivot_data = pivot_data.reset_index()

# Plotting
pivot_data.set_index('Condition').plot(kind='bar', stacked=True, figsize=(12, 8), cmap='tab20')
plt.title('Part of Speech Counts per Condition')
plt.ylabel('Count')
plt.xlabel('Condition')
plt.legend(title='Part of Speech')
plt.tight_layout()
plt.show()
