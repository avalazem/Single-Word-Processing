import pandas as pd 

test_data_path = r'C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\English\english_test_data.csv'

# Load the test data
test_data = pd.read_csv(test_data_path)

# Define the function to determine the condition
def determine_condition(row):
    lexicality = 'R' if row['Lexicality'] == 'real' else 'P'
    size = 'S' if row['Size'] == 'short' else 'L'
    frequency = 'L' if row['Frequency'] == 'low' else 'H' if row['Frequency'] == 'high' else ''
    morphology = 'S' if row['Morphology'] == 'simple' else 'C'
    
    return lexicality + size + frequency + morphology

# Apply the function to each row to create the 'Condition' column
test_data['Condition'] = test_data.apply(determine_condition, axis=1)

# Save the updated DataFrame to a new CSV file
test_data.to_csv(test_data_path, index=False)

print(f"Test data with conditions has been saved to {test_data_path}")