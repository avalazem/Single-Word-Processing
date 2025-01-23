import pandas as pd

# Input our csv
input_path = r'C:\Users\ali_a\Desktop\Single Word Processing Stage\Single Word Processing\Data\English Data\English_Stimuli.csv'
input_df = pd.read_csv(input_path)

# Create new dataframe

output_df = pd.DataFrame({
    'item': input_df['Word'],
    'category': input_df['Lexicality'].apply(lambda x: 'P' if x.lower() == 'pseudo' else 'W'), 
})

# Save to new csv in Christophe_Stimulation to use for the stimulation
output_path = r'C:\Users\ali_a\Desktop\Single Word Processing Stage\Single Word Processing\Christophe_Stimulation\lex_run_me_en.csv'
output_df.to_csv(output_path, index=False)

# Confirm
print("Transformed Data Saved to lex_run_me_en.csv")