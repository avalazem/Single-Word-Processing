import sys
import os
import pandas as pd
from expyriment import design, control, stimuli

# Constants
WORD_RESPONSE_KEY = 'f'
QUIT_KEY = 'q'
AUDIO_DURATION = 2000  # milliseconds
SPEECH_WAIT_DURATION = 5000  # milliseconds
WRITING_WAIT_DURATION = 10000  # milliseconds
BREAK_DURATION = 30000  # milliseconds

# Path to the localizer CSV file
localizer_csv_path = r'C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\Stimuli\Localizer_en.csv'

# Load the localizer data
localizer_df = pd.read_csv(localizer_csv_path)

# Initialize the experiment with a larger screen resolution
exp = design.Experiment(name="Single Word Processing Localizer", text_size = 40)
control.initialize(exp)

# Display instructions for the audio run
instructions = stimuli.TextScreen(
    "Audio Run Instructions",
    """You will now be presented with audio. Listen and stay still!
    
    \n\nPress the space bar to begin."""
)
instructions.present()
exp.keyboard.wait_char(" ")

# Path to the audio files
audio_folder_path = r'C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\Stimuli\reversed_audio_files_wav'

# Create the trial sequence with the shuffled stimuli
for index, row in localizer_df.iterrows():
    stimulus = row['Stimuli']
    stimulus_type = row['Stimuli Type']
    word = stimulus.split('_')[1]  # Extract the word from the file name

    cue = stimuli.FixCross(size=(50, 50), line_width=4)
    cue.present()
    exp.clock.wait(500)  # Fixation duration (500 ms)

    if stimulus_type == 'Audio':
        # Present audio files
        audio_path = os.path.join(audio_folder_path, stimulus)
        
        # Play audio
        audio_stimulus = stimuli.Audio(audio_path)
        audio_stimulus.play()
        
        # Wait for the specified duration or until the audio is finished
        exp.clock.wait(AUDIO_DURATION)

control.end()