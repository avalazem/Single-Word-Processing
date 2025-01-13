import sys
import random
import pandas
from expyriment import design, control, stimuli
import os
from pydub import AudioSegment  # Import pydub for audio processing

WORD_RESPONSE_KEY = 'f'
QUIT_KEY = 'q'
STIMULUS_DURATION = 200  # in milliseconds
SPEECH_WAIT_DURATION = 5000  # in milliseconds
WRITING_WAIT_DURATION = 10000  # in milliseconds

if len(sys.argv) < 2:
    print("""Usage: [python] swp.py CSVFILE

where CSVFILE is a comma-separated file with columns:
    - `Word` (containing a word)
    - `Condition` (containing one of 12 conditions)
    - `Audio` (audio file name)
    """)
    sys.exit(1)

stim_file = sys.argv[1]  # reads second argument from command line

exp = design.Experiment(name="Single Word Processing", text_size=40)
control.initialize(exp)

# Prepare the stimuli
materials = pandas.read_csv(stim_file)
words = materials['Word'].tolist()  # List of words
conditions = materials['Condition'].tolist()  # List of conditions
audio_files = materials['Audio'].tolist()  # List of corresponding audio files

# Create distinct runs
runs = {
    "word_covert_speech": [],
    "word_write": [],
    "audio_covert_speech": [],
    "audio_write": []
}

# Organize stimuli into respective runs
for word, condition, audio in zip(words, conditions, audio_files):
    runs["word_covert_speech"].append((word, condition, audio, 'word', 'Covert Speech'))
    runs["word_write"].append((word, condition, audio, 'word', 'Write'))
    runs["audio_covert_speech"].append((word, condition, audio, 'audio', 'Covert Speech'))
    runs["audio_write"].append((word, condition, audio, 'audio', 'Write'))

# Split runs into mini-runs
def split_into_mini_runs(trials, num_mini_runs):
    random.shuffle(trials)  # Shuffle the trials
    return [trials[i::num_mini_runs] for i in range(num_mini_runs)]

# Path to the audio files
audio_folder_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\Stimuli\audio_files_wav"

# Shuffle the main runs
main_run_order = list(runs.keys())
random.shuffle(main_run_order)

# Instructions for each run type
run_instructions_dict = {
    "word_covert_speech": f"""You will now be presented with written words on the screen. 
    
Your task is to read them silently (covertly), without moving your lips or making any sound, within 5 seconds.

When finished, press '{WORD_RESPONSE_KEY.lower()}'.""",

    "word_write": f"""You will now be presented with written words on the screen.
     
Your task is to write them down on the provided sheet as quickly and accurately as possible, within 10 seconds

When finished, press '{WORD_RESPONSE_KEY.lower()}'.""",
    "audio_covert_speech": f"""You will now hear spoken words through the audio system. 
    
Your task is to listen carefully and repeat them silently (covertly), without moving your lips or making any sound, within 5 seconds.

When finished, press '{WORD_RESPONSE_KEY.lower()}'.""",
    "audio_write": f"""You will now hear spoken words through the audio system.
     
Your task is to write them down on the provided sheet as quickly and accurately as possible, within 10 seconds.

When finished, press '{WORD_RESPONSE_KEY.lower()}'."""}
# Start the experiment
control.start(skip_ready_screen=True)

instructions = stimuli.TextScreen("Instructions",
     f"""You will be going through 4 main runs, split into either 2 or 4 mini-runs, depending on the task.
        
        Each mini-run will take 4 minutes.
    
    Each run will have a:
    
         - Word (VISUAL or AUDITORY) 
         - Task (COVERT SPEECH or WRITING). 

    Make sure to keep still and focus on the task. Thank you for your participation!
    
    When ready, press the space bar to start.""")

instructions.present()
exp.keyboard.wait_char(" ")

for main_run_index, run_name in enumerate(main_run_order, start=1):
    # Display instructions for the main run with "(Part X/4)"
    main_run_instructions = stimuli.TextScreen(
        f"{run_name.replace('_', ' ').capitalize()} (Part {main_run_index}/4)",
        f"{run_instructions_dict[run_name]}\n\nPress the space bar to begin."
    )

    # THE FOLLOWING WON'T WORK, NOT SURE IF/HOW EXPYRIMENT ALLOWS FOR SIMULTANEOUS TEXT/IMAGE
     
    # Set up the image based on the task
    image_folder_path = r'C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\Images'
    
    # Choose image based on task (Writing or Speech)
    if "write" in run_name:
        image_path = os.path.join(image_folder_path, "pencil.png")
    else:
        image_path = os.path.join(image_folder_path, "closed_mouth.png")

    # Load the image if it exists
    if os.path.exists(image_path):
        image = stimuli.Picture(image_path)
        image.position = (0, -100)  # Adjust the Y-axis for positioning below the text instructions

        # Plot the image on top of the TextScreen
        main_run_instructions.plot(image)  # This will overlay the image onto the text screen

    # Present the stimuli
    main_run_instructions.present()
    
    # Wait for the space bar press to proceed
    exp.keyboard.wait_char(" ")
    
    
    # Split the current run into mini-runs
    num_mini_runs = 4 if "write" in run_name else 2
    mini_runs = split_into_mini_runs(runs[run_name], num_mini_runs)

    for mini_run_index, mini_run in enumerate(mini_runs, start=1):
        
        # Present trials in the mini-run
        for word, condition, audio, stimulus_type, response_mode in mini_run:
            cue = stimuli.FixCross(size=(50, 50), line_width=4)
            cue.present()
            exp.clock.wait(500)  # Fixation duration (500 ms)

            # Present the stimulus and a blank screen afterward
            
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

            

        # Add a one-minute break with an automatic timer between mini-runs
        if mini_run_index < num_mini_runs:
            for remaining_seconds in range(60, 0, -1):
                break_message = stimuli.TextScreen("Break",
                    f"Take a one-minute break. Relax and prepare for the next part.\n\n"
                    f"The next part will start automatically in {remaining_seconds} seconds.")
                break_message.present()
                exp.clock.wait(1000)  # Wait 1 second (1000 ms)

control.end()
