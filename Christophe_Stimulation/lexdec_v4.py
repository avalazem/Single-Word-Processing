import sys
import random
import pandas
from expyriment import design, control, stimuli
import os

WORD_RESPONSE_KEY = 'f'
QUIT_KEY = 'q'
STIMULUS_DURATION = 200  # in milliseconds
SPEECH_WAIT_DURATION = 5000  # in milliseconds
WRITING_WAIT_DURATION = 10000  # in milliseconds

if len(sys.argv) < 2:
    print("""Usage: [python] lexdec_v4.py CSVFILE

where CSVFILE is a comma-separated file with columns:
    - `Word` (containing a word)
    - `Condition` (containing one of 12 conditions)
    - `Audio` (audio file name)
    """)
    sys.exit(1)

stim_file = sys.argv[1]

exp = design.Experiment(name="Single Word Processing with Audio", text_size=40)
control.initialize(exp)

# Prepare the stimuli
materials = pandas.read_csv(stim_file)
words = materials['Word'].tolist()  # List of words
conditions = materials['Condition'].tolist()  # List of conditions
audio_files = materials['Audio'].tolist()  # List of corresponding audio files

# Create a list of trials with each word appearing four times:
# 1. Word + Covert Speech
# 2. Word + Write
# 3. Audio + Covert Speech
# 4. Audio + Write

trials = []

# Add trials for each word (both visual and auditory stimuli, with both Covert Read and Write)
for word, condition, audio in zip(words, conditions, audio_files):
    trials.append((word, condition, audio, 'word', 'Covert Speech'))  # Word stimulus + Covert Read
    trials.append((word, condition, audio, 'word', 'Write'))  # Word stimulus + Write
    trials.append((word, condition, audio, 'audio', 'Covert Speech'))  # Audio stimulus + Covert Read
    trials.append((word, condition, audio, 'audio', 'Write'))  # Audio stimulus + Write

# Shuffle the trials to randomize the order
random.shuffle(trials)

cue = stimuli.FixCross(size=(50, 50), line_width=4)
instructions = stimuli.TextScreen("Instructions",
    f"""When presented a stimulus, your task is to, as quickly as possible, either covert speech or write.

    When finished, press '{WORD_RESPONSE_KEY.upper()}'. 

    Press the space bar to start.""")

exp.add_data_variable_names(['word', 'condition', 'audio', 'stimulus_type', 'response_mode', 'response_key', 'reaction_time'])

control.start(skip_ready_screen=True)
instructions.present()
exp.keyboard.wait_char(" ")

# Path to the audio files
audio_folder_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\audio_files_wav"  # Adjust based on your audio files location

# Create the trial sequence with the shuffled word, condition, audio, and response mode
for word, condition, audio, stimulus_type, response_mode in trials:
    cue.present()
    exp.clock.wait(500)  # Fixation duration (500 ms)

    if stimulus_type == "word":
        # Present the stimulus (word) for 200 ms
        word_stimulus = stimuli.TextLine(word)
        word_stimulus.present()
        exp.clock.wait(STIMULUS_DURATION)
        
        # Present blank screen after word stimulus
        blankscreen = stimuli.BlankScreen()
        blankscreen.present()
        exp.clock.wait(500)  # Wait for 500 ms before showing next task
    
    elif stimulus_type == "audio":
        # Present audio files
        audio_path = os.path.join(audio_folder_path, audio)
        
        # Play audio
        audio_stimulus = stimuli.Audio(audio_path)
        audio_stimulus.play()
        
        # Wait for the specified duration or until the audio is finished
        exp.clock.wait(STIMULUS_DURATION)

    # After stimulus presentation, wait 500 ms before presenting task (Covert Speech / Write)
    exp.clock.wait(500)

    # Present the Covert Speech / Write screen
    if response_mode == "Covert Speech":
        response_text = stimuli.TextLine("SPEECH")
    elif response_mode == "Write":
        response_text = stimuli.TextLine("WRITE")
    
    response_text.present()
    
    # Define the response time
    response_time = SPEECH_WAIT_DURATION if response_mode == "Covert Speech" else WRITING_WAIT_DURATION
    
    # Record the start time of the response
    start_time = exp.clock.time
    
    # Wait for a response (up to the respective times)
    key, rt = exp.keyboard.wait_char([WORD_RESPONSE_KEY, QUIT_KEY], duration = response_time)
    
    # If the participant pressed a key (e.g., 'f'), continue to wait the remaining time
    if key == WORD_RESPONSE_KEY:
        exp.clock.wait(response_time - rt)

    # Save data (whether the participant pressed 'f' or quit)
    exp.data.add([word, condition, audio, stimulus_type, response_mode, key, rt])

    if key == QUIT_KEY:  # Exit the experiment if 'q' is pressed
        break

control.end()