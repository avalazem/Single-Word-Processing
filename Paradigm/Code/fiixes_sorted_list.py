import pandas as pd


# Read excel sheets with affixes
input_csv_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\French\Morpholex-FR\Morpholex_FR.xlsx"

suffix_df = pd.read_excel( input_csv_path, "suffixes")
prefix_df = pd.read_excel( input_csv_path, "prefixes")


# Rename the first column header to 'suffix'
suffix_df.rename(columns={suffix_df.columns[0]: 'Suffix'}, inplace=True)
prefix_df.rename(columns={prefix_df.columns[0]: 'Prefix'}, inplace=True)


# Remove the surrounding << characters from the 'suffix' and 'prefix' columns
suffix_df['Suffix'] = suffix_df['Suffix'].str.replace('<<', '').str.replace('>>', '')
prefix_df['Prefix'] = prefix_df['Prefix'].str.replace('<<', '').str.replace('>>', '')


# Extract desired columns 
suffix_df = suffix_df[['Suffix', 'summed_freq']]
prefix_df = prefix_df[['Prefix', 'summed_freq']]


# Add a 'Type' column to each DataFrame
suffix_df['Type'] = 'Suffix'
prefix_df['Type'] = 'Prefix'

# Rename the 'Suffix' and 'Prefix' columns to 'Affix'
suffix_df.rename(columns={'Suffix': 'Affix'}, inplace=True)
prefix_df.rename(columns={'Prefix': 'Affix'}, inplace=True)

# Combine both DataFrames
combined_df = pd.concat([suffix_df, prefix_df])

# Reorder columns to have 'Affix', 'Type', and 'summed_freq'
combined_df = combined_df[['Affix', 'Type', 'summed_freq']]

combined_df = combined_df.sort_values( by = 'summed_freq', ascending= False)


combined_df.to_excel(r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\French\Morpholex-FR\Affixes_combined.xlsx", index= False)

print("Succesfully exported Affixes_combined.xlsx!")