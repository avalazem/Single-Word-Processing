"""Synthesizes speech from the input string of text or ssml.
Make sure to be working in a virtual environment.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
import os
import pandas as pd
from google.cloud import texttospeech
from google.auth.credentials import Credentials
from google.auth.transport.requests import Request

class APIKeyCredentials(Credentials):
    def __init__(self, api_key):
        super().__init__()
        self._api_key = api_key

    def refresh(self, request):
        pass

    def apply(self, headers, token=None):
        headers['x-goog-api-key'] = self._api_key

# Set API key (Thanks Louis!!)
api_key = "API_KEY"

# Create credentials from the API key
credentials = APIKeyCredentials(api_key)

# Instantiates a client with the API key
client = texttospeech.TextToSpeechClient(credentials=credentials)



# Read the CSV file
input_csv_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Visual\French\french_stimuli - French_Stimuli_Real_Options.csv"
df = pd.read_csv(input_csv_path)

# # For all words in the dataframe!!!

# # Iterate over each row in the 'Word' column of the dataframe
# for index, row in df.iterrows():
#     word = row['Word']
#     gender = "MALE_G" # Set gender

#     # Set the text input to be synthesized
#     synthesis_input = texttospeech.SynthesisInput(text=word)

#     # Build the voice request, select the language code ("en-US") and the ssml
#     # voice gender ("neutral")
#     voice = texttospeech.VoiceSelectionParams(
#         language_code="fr-FR", # 'en-US' for English 'fr-FR' for French
#         name="fr-FR-Wavenet-G"  # Specify the voice name 
#         # For English use I for male and G for female!!!
#         ## For English 'daip' pronounce 'p' D for male C for female 
#         # For French use C for female and G for male!!!
#     )

#     # Select the type of audio file you want returned
#     audio_config = texttospeech.AudioConfig(
#         audio_encoding=texttospeech.AudioEncoding.LINEAR16
#     )

#     # Perform the text-to-speech request on the text input with the selected
#     # voice parameters and audio file type
#     response = client.synthesize_speech(
#         input=synthesis_input, voice=voice, audio_config=audio_config
#     )

#     # The response's audio_content is binary.
#     output_folder = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Auditory\French\Google_Cloud_French"
#     output_path = os.path.join(output_folder, f"{word}_{gender}.wav")

#     with open(output_path, "wb") as out:
#     # Write the response to the output file

#         out.write(response.audio_content)
#         print(f'Audio content written to file "{output_path}!"')

#     # Output directory
#     output_audio_dir = r'C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Paradigm\Audio_Files_Google_Cloud'
#     os.makedirs(output_audio_dir, exist_ok=True)

    
      
   
# For indivudual words!!!

# Set word babee
word = "tyrannie"
#gender = "FEMALE_C"
gender = "MALE_G"

# Set the text input to be synthesized
synthesis_input = texttospeech.SynthesisInput(text=word)

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="fr-FR", # 'en-US' for English 'fr-FR' for French
    #name="fr-FR-Wavenet-C" # Specify the voice name (FEMALE)
    name="fr-FR-Wavenet-G" # MALE 
    # For English use I for male and G for female!!!
    ## For English 'daip' pronounce 'p' D for male C for female 
    # For French use C for female and G for male!!!
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.LINEAR16
)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# The response's audio_content is binary.
output_folder = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\SWP_Pilot_1\training\Input_Data\Audio_Files"
output_path = os.path.join(output_folder, f"{word}_{gender}.wav")

with open(output_path, "wb") as out:
# Write the response to the output file

    out.write(response.audio_content)
    print(f'Audio content written to file "{output_path}!"')

# Output directory
output_audio_dir = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\SWP_Pilot_1\training\Input_Data\Audio_Files"
os.makedirs(output_audio_dir, exist_ok=True)
