'''
From Christophe Pallier's (Christophe@pallier.org) 
lexdec_v3.py (https://github.com/chrplr/PCBS/blob/master/experiments/xpy_lexical_decision/lexdec_v3.py)
using the expyriment module (https://github.com/chrplr/expyriment)

Project: Single Word Processing (https://github.com/avalazem/Single-Word-Processing)
Author: Ali Al-Azem
Supervisor: Yair Lakretz

'''
import sys
import random
import pandas as pd
from expyriment import design, control, stimuli
import os
from pydub import AudioSegment  # Import pydub for audio processing

# Constants
WORD_RESPONSE_KEY = 'f'
QUIT_KEY = 'q'
STIMULUS_DURATION = 200  # in milliseconds
SPEECH_WAIT_DURATION = 5000  # in milliseconds
WRITING_WAIT_DURATION = 7000  # in milliseconds
VISUAL_WAIT_DURATION = 200

# Initialize the experiment
exp = design.Experiment(name="Single Word Processing", text_size=40)
control.initialize(exp)

# Import the localizer CSV file
stimuli_df = pd.read_csv(r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\Stimuli\Localizer_en.csv")

# Initialize the runs dictionary with all necessary keys
runs = {
    "audio": [],
    "image": [],
    "covert_speech": [],
    "writing": []
}

# Iterate through each row of the CSV
for _, row in stimuli_df.iterrows():
    stimulus = row['Stimuli']        # The stimulus (word, image, or audio file)
    stimulus_type = row['Stimuli Type'].lower()  # The type of stimulus (audio, image, covert_speech, writing)
    
    # Add stimuli to appropriate run based on stimulus type
    if stimulus_type == 'audio':
        runs["audio"].append(stimulus)
    elif stimulus_type == 'image':
        runs["image"].append(stimulus)
    elif stimulus_type == 'covert_speech':
        runs["covert_speech"].append(stimulus)
    elif stimulus_type == 'writing':
        runs["writing"].append(stimulus)

# Path to the audio files
audio_folder_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\Stimuli\reversed_audio_files_wav"

# Path to image files
image_folder_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\Images\Localizer_Images"

# Path to instruction images
instruction_image_folder = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\Images\Instructions"

# Start the experiment
control.start(skip_ready_screen=True)

# Display general instructions
instructions = stimuli.Picture(r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\Images\Instructions\localizer_instructions.png")
instructions.scale_to_fullscreen()
instructions.present()
exp.keyboard.wait_char(" ")


# Path to "press.wav" audio file
press_audio_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\audio_files_wav\press.wav"

# Counter to track when to add "press" prompts
audio_press_counter = 0
visual_press_counter = 0

# Present all runs
for i, (run_name, run_data) in enumerate(runs.items()):
    # Display image-based instructions if available
    image_path = os.path.join(instruction_image_folder, f"{run_name}_instructions.png")
    if os.path.exists(image_path):
        instructions = stimuli.Picture(image_path)
        instructions.scale_to_fullscreen()
        instructions.present()
        exp.keyboard.wait_char(" ")

    # Present each trial in the mini-run
    for index, stimulus in enumerate(run_data):
        cue = stimuli.FixCross(size=(50, 50), line_width=4)
        cue.present()
        exp.clock.wait(500)  # Fixation duration (500 ms)

        # Add "press" prompt dynamically for audio and visual runs
        add_press_prompt = False
        if run_name == "audio":
            audio_press_counter += 1
            if audio_press_counter >= random.randint(1, 5):
                add_press_prompt = True
                audio_press_counter = 0
        elif run_name == "image":
            visual_press_counter += 1
            if visual_press_counter >= random.randint(1, 5):
                add_press_prompt = True
                visual_press_counter = 0

        # Handle visual stimuli
        if run_name == "image":
            # Show image
            image_path = os.path.join(image_folder_path, stimulus)
            image_stimulus = stimuli.Picture(image_path)
            image_stimulus.present()
            
            # Wait for VISUAL_DURATION while checking for QUIT_KEY
            start_time = exp.clock.time
            while exp.clock.time - start_time < VISUAL_WAIT_DURATION:
                key = exp.keyboard.check()
                if key == QUIT_KEY:
                    control.end()
                    sys.exit()
            stimuli.BlankScreen().present()
            
            # If "press" prompt is triggered, display "press" as text
            if add_press_prompt:
                stimuli.BlankScreen().present() # Clear previous cue
                exp.clock.wait(2000) # Still wait as if in a normal word sequence
                cue = stimuli.FixCross(size=(50, 50), line_width=4)
                cue.present()
                exp.clock.wait(500)  # Fixation duration (500 ms)
                press_stimulus = stimuli.TextLine("press")
                press_stimulus.present()
                exp.clock.wait(STIMULUS_DURATION)
                stimuli.BlankScreen().present()
                
                # Wait for 'press'
                response_time = 5000 # Wait up to 5 seconds 
                start_time = exp.clock.time
                key, rt = exp.keyboard.wait_char([WORD_RESPONSE_KEY, QUIT_KEY], duration=response_time)

                if key == QUIT_KEY:
                    control.end()
                    sys.exit()
                    
                # Save trial data
                exp.data.add(['press', run_name, key, rt])
                
                
            # Wait a few seconds between each stimuli
            exp.clock.wait(2000)

        # Handle audio stimuli
        elif run_name == "audio":
            # Play the audio stimulus
            audio_path = os.path.join(audio_folder_path, stimulus)
            audio_clip = AudioSegment.from_file(audio_path)
            audio_duration = len(audio_clip)

            audio_stimulus = stimuli.Audio(audio_path)
            audio_stimulus.play()
            exp.clock.wait(audio_duration)
            stimuli.BlankScreen().present()

            # If "press" prompt is triggered, play the "press.wav" audio file
            if add_press_prompt:
                exp.clock.wait(2000) # Still wait as if in a normal word sequence
                cue = stimuli.FixCross(size=(50, 50), line_width=4)
                cue.present()
                cue = stimuli.FixCross(size=(50, 50), line_width=4)
                cue.present()
                exp.clock.wait(500)
                
                press_audio = stimuli.Audio(press_audio_path)
                press_audio_clip = AudioSegment.from_file(press_audio_path)
                press_audio_duration = len(press_audio_clip)
                press_audio.play()
                exp.clock.wait(press_audio_duration)  # Wait for the "press" audio to finish
                stimuli.BlankScreen().present()

                # Wait for 'press'
                response_time = 5000 # Wait up to 5 seconds 
                start_time = exp.clock.time
                key, rt = exp.keyboard.wait_char([WORD_RESPONSE_KEY, QUIT_KEY], duration=response_time)

                if key == QUIT_KEY:
                    control.end()
                    sys.exit()

                # Save trial data
                exp.data.add(['press', run_name, key, rt])
                    
            # Wait a few seconds between each stimuli
            exp.clock.wait(2000)

        # Handle other stimulus types (covert_speech, writing)
        elif run_name == "covert_speech":
            # Wait for participant response
            response_time = SPEECH_WAIT_DURATION
            start_time = exp.clock.time
            key, rt = exp.keyboard.wait_char([WORD_RESPONSE_KEY, QUIT_KEY], duration=response_time)

            if key == QUIT_KEY:
                control.end()
                sys.exit()

            if key == WORD_RESPONSE_KEY:
                rt = exp.clock.time - start_time  # Record reaction time

            # Collect data
            exp.data.add([stimulus, run_name, key, rt])

        elif run_name == "writing":
            # Wait for participant response
            response_time = WRITING_WAIT_DURATION
            start_time = exp.clock.time
            key, rt = exp.keyboard.wait_char([WORD_RESPONSE_KEY, QUIT_KEY], duration=response_time)

            if key == QUIT_KEY:
                control.end()
                sys.exit()

            if key == WORD_RESPONSE_KEY:
                rt = exp.clock.time - start_time  # Record reaction time

            # Collect data
            exp.data.add([stimulus, run_name, key, rt])

    # Break between runs
    if i < len(runs) - 1:
        for remaining_seconds in range(1, 0, -1):
            break_message = stimuli.TextScreen(
                "Break",
                f"Take a 30-second break. Relax and prepare for the next part.\n\n"
                f"The next part will start automatically in {remaining_seconds} seconds."
            )
            break_message.present()
            exp.clock.wait(1000)  # Wait 1 second (1000 ms)

# Display thank you instructions
thank_you_message = stimuli.Picture(r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\Images\Instructions\end_of_localizer.png")
thank_you_message.scale_to_fullscreen()
thank_you_message.present()
exp.keyboard.wait_char(" ")

control.end()
