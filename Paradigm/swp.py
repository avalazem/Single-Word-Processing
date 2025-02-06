'''
From Christophe Pallier's (Christophe@pallier.org) 
lexdec_v3.py (https://github.com/chrplr/PCBS/blob/master/experiments/xpy_lexical_decision/lexdec_v3.py)
using the expyriment module (https://github.com/chrplr/expyriment)

Project: Single Word Processing (https://github.com/avalazem/Single-Word-Processing)
Author: Ali Al-Azem
Supervisor: Yair Lakretz

'''
import sys
import pandas as pd
from expyriment import design, control, stimuli
import os
from pydub import AudioSegment  # Import pydub for audio processing

# Constants
WORD_RESPONSE_KEY = 'y'
QUIT_KEY = 'q'
STIMULUS_DURATION = 200  # in milliseconds
FIXATION_DURATION = 500 
TRIGGER_KEY = 't' # For the fMRI machine
CONTROLLER_KEY = ' ' # For who runs the paradigm
WAIT_FOR_FINAL_TRIGGER = 10000 # 10 seconds

# Check for correct usage
if len(sys.argv) < 2:
    print("""Usage: [python] swp.py CSVFILE

where CSVFILE is a comma-separated file with columns:
    - `Word` (containing a word)
    - `Condition` (containing one of 12 conditions)
    - `Audio File` (audio file name)
    - `Trial Duration`
    - `Input Modality` (Visual or Audio)
    - `Output Modality  (Speech or Write)
    """)
    sys.exit(1)

stim_file = sys.argv[1]  # Read second argument from command line

# Path to the audio files
audio_folder_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Paradigm\Stimuli\Audio_Files_Google_Cloud"

# Path to run instructions image folder
instruction_image_folder = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Paradigm\Images\Instructions"

# Path to Beginning Instructions
# welcome_instructions_png = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Paradigm\Images\Instructions\instructions.png"

# Path to Thank you ending picture
# thank_you_png = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Paradigm\Images\Instructions\thank_you.png"


# Function to display instructions based on modalities
def display_instructions(exp, input_modality, output_modality, instructions_folder):
    instruction_image_path = f"{instructions_folder}/{input_modality}_{output_modality}.png"
    instructions = stimuli.Picture(instruction_image_path)
    instructions.scale_to_fullscreen()
    instructions.present()
    
    # Wait for controller to press CONTROLLER_KEY
    exp.keyboard.wait_char(CONTROLLER_KEY)


# Function to display word or play audio
def display_or_play(exp, row):
    

    if row['Input Modality'] == 'Visual':
        
        # Present fixation cross
        cue = stimuli.FixCross(size=(40, 40), line_width=4)
        cue.present()
        exp.clock.wait(FIXATION_DURATION)  # Fixation duration (500 ms)
        stimuli.BlankScreen().present()
        
        # Present Word 
        word_stimulus = stimuli.TextLine(row['Word'])
        word_stimulus.present()
        
        # Wait for STIMULUS_DURATION while checking for QUIT_KEY
        start_time = exp.clock.time
        while exp.clock.time - start_time < STIMULUS_DURATION:
            key = exp.keyboard.check()
            if key == QUIT_KEY:
                control.end()
                sys.exit()
        stimuli.BlankScreen().present()
        
        # After word is displayed re-display  fixation cross
        cue = stimuli.FixCross(size=(40, 40), line_width=4)
        cue.present()
               
    elif row['Input Modality'] == 'Audio':
        
        # Display fixation cross throughout audio trial duration (including when audio is being played)
        cue = stimuli.FixCross(size=(40, 40), line_width=4)
        cue.present()
                    
        audio_path = os.path.join(audio_folder_path, row['Audio File'])
        if not os.path.exists(audio_path):
            print(f"❌ Audio file {audio_path} not found.")
        audio_clip = AudioSegment.from_file(audio_path)
        AUDIO_DURATION = len(audio_clip)
        audio_stimulus = stimuli.Audio(audio_path)
        audio_stimulus.play()
        
        # Wait for AUDIO_DURATION while checking for QUIT_KEY
        start_time = exp.clock.time
        while exp.clock.time - start_time < AUDIO_DURATION:
            key = exp.keyboard.check()
            if key == QUIT_KEY:
                control.end()
                sys.exit()   

# Function to handle participant response
def handle_response(exp, row):
    if row['Input Modality'] == 'Visual':
        response_time = 1000 * row['Trial Duration'] - (STIMULUS_DURATION + FIXATION_DURATION) # To ensure trial time
    elif row['Input Modality'] == 'Audio':
        audio_path = os.path.join(audio_folder_path, row['Audio File'])
        audio_clip = AudioSegment.from_file(audio_path)
        AUDIO_DURATION = len(audio_clip)
        # Define Response time To ensure SOA is EXACTLY Jitter Duration
        response_time = 1000 * row['Trial Duration'] - (AUDIO_DURATION + FIXATION_DURATION) # To ensure trial time

    key, rt = exp.keyboard.wait_char([WORD_RESPONSE_KEY, QUIT_KEY], duration=response_time)
    
    # Handle quit key
    if key == QUIT_KEY:
        control.end()
        sys.exit()

    # If a valid response is made, compute reaction time
    if key == WORD_RESPONSE_KEY:
        exp.clock.wait(response_time - rt) # Record reaction time

    # Extract the name of the stim_file to save
    csv_name = os.path.basename(stim_file).replace('.csv', '')
    
    # Collect data babee
    exp.data.add([csv_name, row['Word'], row['Input Modality'], row['Output Modality'], key, rt])
    

    
    
# Main function to run the experiment
def run_experiment(stim_file, audio_folder_path, instruction_image_folder):
    # Initialize the experiment
    exp = design.Experiment(name="Single Word Processing", text_size=40)
    control.initialize(exp)


    # Read the CSV file
    df = pd.read_csv(stim_file)

    # Start the experiment
    control.start(skip_ready_screen=True)
    

    # Display run instructions based on the first row's modalities
    first_row = df.iloc[0]
    display_instructions(exp, first_row['Input Modality'], first_row['Output Modality'], instruction_image_folder)

    # Display 'Get Ready...' 
    word_stimulus = stimuli.TextLine('Get Ready...')
    word_stimulus.present()
    
    # Wait for trigger to start
    exp.keyboard.wait_char(TRIGGER_KEY)
    
    # Clear after trigger is sent
    stimuli.BlankScreen().present()
    
    # Start a clock to keep track of time between first and last 't' (while fMRI is scanning)
    start_time = exp.clock.time
    
    # Record time when first t is played
    exp.data.add([TRIGGER_KEY, start_time])
    
    
    # Iterate through each row of the CSV file
    for _, row in df.iterrows():
        # Clear the keyboard buffer before waiting for participant response
        exp.keyboard.clear()

        # Display word or play audio based on Input Modality
        display_or_play(exp, row)

        # Handle participant response based on Output Modality
        handle_response(exp, row)


    # Wait for trigger to end after final stimuli is played
    exp.keyboard.wait_char(TRIGGER_KEY, duration = WAIT_FOR_FINAL_TRIGGER) # Wait one full TR after final stimulus
    
    # Record time when last t is played
    end_time = exp.clock.time
    duration = end_time - start_time
    exp.data.add([TRIGGER_KEY, end_time])
    exp.data.add(['Duration between Triggers: ', duration]) # Record Total duration of fMRI Scan

    
    # End the experiment
    control.end()
    

# Run experiment!!
run_experiment(stim_file, audio_folder_path, instruction_image_folder)