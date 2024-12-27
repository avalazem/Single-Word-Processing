import pandas as pd
import os

# List of CSV file paths to combine
csv_files = [r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/French Data/deliane_french_real/ppr.csv',
             r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/French Data/deliane_french_real/pr_long.csv',
             r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/French Data/deliane_french_real/pr.csv',
             r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/French Data/deliane_french_real/prs.csv',
             r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/French Data/deliane_french_real/prss.csv',
             r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/French Data/deliane_french_real/rs.csv',
             r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/French Data/deliane_french_real/rss.csv',
             r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/French Data/deliane_french_real/rsss.csv']  

# Columns to keep
columns_to_keep = ['Word', 'Root', 'Wordlength', 'Frequency']

# Initialize an empty list to store DataFrames
dataframes = []

for file in csv_files:
    # Read each CSV file
    df = pd.read_csv(file)
    
    # Filter the columns
    filtered_df = df[columns_to_keep]
    
    # Add a new column for the condition based on the file name + lexicality == real
    filtered_df['Condition'] = os.path.basename(file).replace('.csv', '')  # Strip ".csv" from the file name
    filtered_df['Lexicality'] = 'real'  # Add Lexicality column with value "real"
    
    # Set Morphological Complexity column
    if file == 'file_simple.csv':  # Check if the file is the specific one
        filtered_df['Morphological Complexity'] = 'simple'
    else:
        filtered_df['Morphological Complexity'] = 'complex'
    
    
    # Append the filtered DataFrame to the list
    dataframes.append(filtered_df)

# Concatenate all DataFrames into one
combined_df = pd.concat(dataframes, ignore_index=True)

# Save the combined DataFrame to a new CSV file
output_file = r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/French Data/deliane_french_real/deliane_combined.csv'
combined_df.to_csv(output_file, index=False)

print(f"Combined data saved to {output_file}")


# Now adding the r case

# File to add
new_file = r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/French Data/deliane_french_real/r.csv'

# Columns to keep
columns_to_keep = ['Word', 'Wordlength', 'Frequency']

# Read the new CSV file
new_df = pd.read_csv(new_file)

# Filter the necessary columns
filtered_new_df = new_df[columns_to_keep].copy()

# Add a blank Root column
filtered_new_df['Root'] = None  # Blank Root values

# Add the condition column (file name without the ".csv")
filtered_new_df['Condition'] = 'r'

# Add Lexicality column with value "real"
filtered_new_df['Lexicality'] = 'real'

# Set Morphological Complexity column to "simple"
filtered_new_df['Morphological Complexity'] = 'simple'

# Create a 'Length' column based on the length of the 'Word' column
filtered_new_df['Length'] = combined_df['Wordlength'].apply(lambda x: 'short' if x < 7 else 'long')


# Combine the datasets
final_combined_df = pd.concat([combined_df, filtered_new_df], ignore_index=True)

# Create a 'Length' column based on the length of the 'Word' column
final_combined_df['Length'] = combined_df['Wordlength'].apply(lambda x: 'short' if x < 7 else 'long')

# Save the combined dataset to a new CSV
final_combined_df.to_csv(output_file, index=False)
print(f"Final combined data saved to {output_file}")