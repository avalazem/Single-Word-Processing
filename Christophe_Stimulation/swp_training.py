import sys
import random
import pandas
from expyriment import design, control, stimuli
import os
from pydub import AudioSegment  # Import pydub for audio processing

# Constants
WORD_RESPONSE_KEY = 'f'
QUIT_KEY = 'q'
STIMULUS_DURATION = 200  # milliseconds
SPEECH_WAIT_DURATION = 5000  # milliseconds
WRITING_WAIT_DURATION = 10000  # milliseconds
BREAK_DURATION = 30000  # milliseconds

# Argument check
if len(sys.argv) < 2:
    print("""Usage: [python] swp.py CSVFILE

where CSVFILE is a comma-separated file with columns:
    - `Word` (containing a word)
    - `Condition` (containing one of 12 conditions)
    - `Audio` (audio file name)
    """)
    sys.exit(1)

stim_file = sys.argv[1]

# Initialize experiment
exp = design.Experiment(name="Single Word Processing", text_size=40)
control.initialize(exp)

# Load stimuli from the CSV file
materials = pandas.read_csv(stim_file)
words = materials['Word'].tolist()
conditions = materials['Condition'].tolist()
audio_files = materials['Audio'].tolist()

# Organize stimuli into respective runs
runs = {
    "word_covert_speech": [(word, condition, audio, 'word', 'Covert Speech') for word, condition, audio in zip(words, conditions, audio_files)],
    "word_write": [(word, condition, audio, 'word', 'Write') for word, condition, audio in zip(words, conditions, audio_files)],
    "audio_covert_speech": [(word, condition, audio, 'audio', 'Covert Speech') for word, condition, audio in zip(words, conditions, audio_files)],
    "audio_write": [(word, condition, audio, 'audio', 'Write') for word, condition, audio in zip(words, conditions, audio_files)]
}

# Shuffle the run order
main_run_order = list(runs.keys())
random.shuffle(main_run_order)

# Instructions for each run type
run_instructions_dict = {
    "word_covert_speech": f"""You will now be presented with written words on the screen. 
    
Your task is to read them silently (covertly), without moving your lips or making any sound, within 5 seconds.

When finished, press '{WORD_RESPONSE_KEY}'.""",

    "word_write": f"""You will now be presented with written words on the screen.
    
Your task is to write them down on the provided sheet as quickly and accurately as possible, within 10 seconds.

When finished, press '{WORD_RESPONSE_KEY}'.""",

    "audio_covert_speech": f"""You will now hear spoken words through the audio system.
     
Your task is to listen carefully and repeat them silently (covertly), without moving your lips or making any sound, within 5 seconds.

When finished, press '{WORD_RESPONSE_KEY}'.""",

    "audio_write": f"""You will now hear spoken words through the audio system.
    
Your task is to write them down on the provided sheet as quickly and accurately as possible, within 10 seconds.

When finished, press '{WORD_RESPONSE_KEY}'."""
}

# Path to the audio files
audio_folder_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\audio_files_wav"

# Start the experiment
control.start(skip_ready_screen=True)

instructions = stimuli.TextScreen(
    "Test Run Instructions",
    f"""**This is a test run.** 
    
    To get comfortable, you will be going through 4 practice runs for around 10 minutes total.
    
    Each run will have a:
    
        - Word (VISUAL or AUDITORY) 
        - Task (COVERT SPEECH or WRITING). 

    Make sure to keep still and focus on the task. Thank you for your participation!
    
    When ready, press the space bar to start."""
)
instructions.present()
exp.keyboard.wait_char(" ")

# Main loop for runs
for run_index, run_name in enumerate(main_run_order[:4], start=1):
    # Display instructions for the run
    run_instructions = stimuli.TextScreen(
        f"Run {run_index}/4: {run_name.replace('_', ' ').capitalize()}",
        run_instructions_dict[run_name] + "\n\nPress the space bar to start."
    )
    run_instructions.present()
    exp.keyboard.wait_char(" ")

    # Present trials in the run
    for word, condition, audio, stimulus_type, response_mode in runs[run_name]:
        cue = stimuli.FixCross(size=(50, 50), line_width=4)
        cue.present()
        exp.clock.wait(500)  # Fixation duration (500 ms)

        if stimulus_type == "word":
                
            # Present word stimulus
            word_stimulus = stimuli.TextLine(word)
            word_stimulus.present()
            exp.clock.wait(STIMULUS_DURATION)
                
            # Clear cue/stimulus
            blank_screen = stimuli.BlankScreen()
            blank_screen.present()

        # Audio stimuli handling    
        elif stimulus_type == "audio":
           
            # Remove the cue
            blank_screen = stimuli.BlankScreen()
            blank_screen.present()

            # Calculate the duration of the audio clip
            audio_path = os.path.join(audio_folder_path, audio)
            audio_clip = AudioSegment.from_file(audio_path)  # Load the audio file
            audio_duration = len(audio_clip)  # Duration in milliseconds

            # Play the audio
            audio_stimulus = stimuli.Audio(audio_path)
            audio_stimulus.play()

            # Wait for the duration of the audio clip
            exp.clock.wait(audio_duration)

            # Ensure the blank screen remains after the audio
            blank_screen.present()

       # Response handling
        response_time = SPEECH_WAIT_DURATION if response_mode == "Covert Speech" else WRITING_WAIT_DURATION
        start_time = exp.clock.time
        key, rt = exp.keyboard.wait_char([WORD_RESPONSE_KEY, QUIT_KEY], duration=response_time)

        if key == QUIT_KEY:
            control.end()
            sys.exit()
                
        if key == WORD_RESPONSE_KEY:
            rt = exp.clock.time - start_time  # Record reaction time (USE IF WANT TO SKIP THROUGH!!)
            # exp.clock.wait(response_time - rt) # Record reaction time (USE FOR ACTUAL EXPERIMENT!!)
                 
        # Add Data Babee   
        exp.data.add([word, condition, audio, stimulus_type, response_mode, key, rt])


    # Break between runs
    if run_index < 4:
        for remaining_seconds in range(60, 0, -1):
            break_message = stimuli.TextScreen("Break",
                f"Take a 1 minute break. Relax and prepare for the next part.\n\n"
                f"The next part will start automatically in {remaining_seconds} seconds.")
            break_message.present()
            exp.clock.wait(1000)  # Wait 1 second (1000 ms)

# End the experiment
control.end()
