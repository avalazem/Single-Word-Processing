import pandas as pd

# Import Sarah's French data
csv_path = r"C:\Users\ali_a\Desktop\Single Word Processing Stage\Single Word Processing\Data\French Data\sarah_french\sarah_french_stimuli_filtered.csv"
stimuli_df=pd.read_csv(csv_path)

# Import real csv to combine
real_csv_path = r"C:\Users\ali_a\Desktop\Single Word Processing Stage\Single Word Processing\Data\French Data\french_stimuli_real.csv"
real_stimuli_df=pd.read_csv(csv_path)


# Filter pseudos
pseudo_df = stimuli_df[stimuli_df['Condition'].str.startswith('pseudo')]

# Replace Sarah's notation to streamline from English data

# Mapping for replacements
replacement_map = {
    "pseudo_court_simple": "PSS",
    "pseudo_court_complexe": "PSC",
    "pseudo_long_simple": "PLS",
    "pseudo_long_complex": "PLC"
}
# Replace
pseudo_df.loc[:, 'Condition'] = pseudo_df['Condition'].replace(replacement_map)

# Now update columns to match french_stimuli_real.csv

# Rename the 'Mot' column to 'Word'
pseudo_df.rename(columns={'Mot': 'Word'}, inplace=True)

# Add 'Wordlength' column
pseudo_df['Wordlength'] = pseudo_df['Word'].apply(len)

# Add 'Lexicality' column (all values set to 'pseudo')
pseudo_df['Lexicality'] = 'pseudo'

# Update 'Length' column based on 'Condition'
pseudo_df['Length'] = pseudo_df['Condition'].apply(
    lambda cond: 'short' if cond in ['PSS', 'PSC'] else 'long'
)

# Update 'Morphology' column based on 'Condition'
pseudo_df['Morphology'] = pseudo_df['Condition'].apply(
    lambda cond: 'simple' if cond in ['PSS', 'PLS'] else 'complex'
)

# Reorder columns to match desired structure
pseudo_df = pseudo_df[['Word', 'Wordlength', 'Lexicality', 'Length', 'Morphology', 'Condition']]

# Export babee
export_csv_path = r"C:\Users\ali_a\Desktop\Single Word Processing Stage\Single Word Processing\Data\French Data\french_stimuli_pseudo.csv"
#pseudo_df.to_csv(export_csv_path, index = False)


# Confirm
print("Succesfully Exported to french_stimuli_pseudo.csv")