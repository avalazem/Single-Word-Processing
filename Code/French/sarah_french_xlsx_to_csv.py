import pandas as pd

# Load the Excel file
excel_file = r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/French Data/sarah_french_stimuli.xlsx'
sheets = pd.read_excel(excel_file, sheet_name=None)  # Load all sheets
output_csv = r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/French Data/sarah_french_stimuli.csv'

# Load all sheets from the Excel file
sheets = pd.read_excel(excel_file, sheet_name=None)  # Load all sheets into a dictionary

# Debug: Print sheet names
print("Sheet names found in the Excel file:")
for sheet_name in sheets.keys():
    print(f"- {sheet_name}")

# Initialize an empty list to store DataFrames
dataframes = []

for sheet_name, sheet_data in sheets.items():
    print(f"\nProcessing sheet: {sheet_name}")  # Debug: Print the sheet name being processed
    
    if sheet_data.empty:
        print(f"Sheet {sheet_name} is empty. Skipping.")
        continue
    
    # Debug: Print sample data from the sheet
    print(f"Sample data from sheet {sheet_name}:")
    print(sheet_data.head())

    # Add the sheet name as the Condition column
    sheet_data['Condition'] = sheet_name
    print(f"Added Condition column for sheet {sheet_name}:")
    print(sheet_data.head())  # Debug: Confirm the Condition column is added

    # Append the updated DataFrame to the list
    dataframes.append(sheet_data)

# Combine all DataFrames into one
if dataframes:  # Ensure there are DataFrames to combine
    combined_df = pd.concat(dataframes, ignore_index=True)
    print("\nCombined DataFrame preview:")
    print(combined_df.head())

    # Save the combined DataFrame as a CSV
    combined_df.to_csv(output_csv, index=False)
    print(f"\nCSV file created successfully: {output_csv}")
else:
    print("\nNo data to combine. Please check the input sheets.")

import pandas as pd

# Load the CSV file into a DataFrame
input_file = output_csv
df = pd.read_csv(input_file)

# Select the desired columns
selected_columns = ['Mot', 'Cat.Gram', 'Fréquence', 'numbre de lettres', 'structure morpho', 'Condition']
filtered_df = df[selected_columns]

# Export the filtered DataFrame to a new CSV file
output_file = r'C:/Users/ali_a/Desktop/Single Word Processing Stage/Single Word Processing/Data/French Data/sarah_french_stimuli_filtered.csv'
filtered_df.to_csv(output_file, index=False)

print(f"Filtered data saved to {output_file}")
