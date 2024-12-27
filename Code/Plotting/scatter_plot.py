import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Load the Excel data
excel_file_path = r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/english_openlex_frequency_data.xlsx'
df_openlex = pd.read_excel(excel_file_path)


# Load the CSV data
csv_file_path = r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/english_test_data.csv'
df_stimuli = pd.read_csv(csv_file_path)

# Add corresponding frequencies from openlex df
merged_df = pd.merge(df_stimuli, df_openlex[['Word', 'Lg10CD']], on='Word', how='left')
df_stimuli['Zipf openlex'] = merged_df['Lg10CD']
#change to "Lg10WF" or other column for different comparisons

#print(list(df_stimuli))
sns.scatterplot(data=df_stimuli, x='Zipf Frequency', y='Zipf openlex')
plt.xlabel('Zipf Frequency')
plt.ylabel('Zipf Openlex "Lg10CD"')
#plt.gca().set_aspect('equal', adjustable='box')
# Determine the overall range
min_limit = min(df_stimuli['Zipf Frequency'].min(), df_stimuli['Zipf openlex'].min())
max_limit = max(df_stimuli['Zipf Frequency'].max(), df_stimuli['Zipf openlex'].max())

# Expand the range to ensure symmetry
padding = 0.5  # Add a small padding for better visualization
range_min = min_limit - padding
range_max = max_limit + padding

# Apply the same range to both axes
plt.xlim(range_min, range_max)
plt.ylim(range_min, range_max)

# Enforce equal aspect ratio
plt.gca().set_aspect('equal', adjustable='box')

# Display the plot
plt.show()