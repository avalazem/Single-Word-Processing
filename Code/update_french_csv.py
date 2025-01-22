import csv
from wordfreq import zipf_frequency

# Path to the input CSV file
input_csv_path = r'C:\Users\ali_a\Downloads\french_stimuli - french_stimuli_real_edited.csv'
# Path to the output CSV file
output_csv_path = r'C:\Users\ali_a\Downloads\french_stimuli - french_stimuli_real_edited.csv'

def update_csv(input_path, output_path):
    with open(input_path, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Word Frequency', 'Letter Count']
        
        rows = list(reader)
        
        for row in rows:
            word = row['Word']
            row['Word Frequency'] = zipf_frequency(word, 'fr')
            row['Letter Count'] = len(word)
        
        with open(output_path, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

if __name__ == "__main__":
    update_csv(input_csv_path, output_csv_path)