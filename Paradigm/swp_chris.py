'''
From Christophe Pallier's (Christophe@pallier.org) 
lexdec_v3.py (https://github.com/chrplr/PCBS/blob/master/experiments/xpy_lexical_decision/lexdec_v3.py)
using the expyriment module (https://github.com/chrplr/expyriment)

Project: Single Word Processing (https://github.com/avalazem/Single-Word-Processing)
Author: Ali Al-Azem
Supervisor: Yair Lakretz

'''


import sys
from pathlib import Path
import pandas as pd
from expyriment import design, control, stimuli, misc, io


DEBUG = False # set to False to run full screen
INITIAL_WAIT = 2000  # 2 seconds
FINAL_WAIT = 10000  # 10 seconds
TEXT_SIZE = 50
TEXT_FONT = 'Inconsolata-Regular.ttf'  # make sure you know which font is used
RESPONSE_KEY = 'y'
STIMULUS_DURATION = 200  # in milliseconds
TRIGGER_KEY = 't' # For the fMRI machine
CONTROLLER_KEY = ' ' # For who runs the paradigm

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
audio_folder_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Paradigm\Input_Data\French\Audio_Files\French"

# Path to run instructions image folder
instruction_image_folder = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Paradigm\Input_Data\French\Images\Instructions_FR"


# Function to display instructions based on modalities
def display_instructions(input_modality, output_modality, instructions_folder):
    instruction_image_path = Path(instructions_folder) / f"{input_modality}_{output_modality}.png"
    instructions = stimuli.Picture(str(instruction_image_path))
    instructions.scale_to_fullscreen()
    instructions.present()
    
################  Setup   ##########################################
exp = design.Experiment(name="Single Word Processing", text_size=40)
if DEBUG:
    control.set_develop_mode()
control.initialize(exp)

# Preparation of the trials
cue = stimuli.FixCross(size=(40, 40), line_width=4)

b = design.Block()
b.add_trials_from_csv_file(stim_file, encoding='utf-8')

prev_onset = INITIAL_WAIT

for trial in b.trials:
    modality = trial.get_factor('Input Modality')
    
    if modality == 'Visual':
        stim = stimuli.TextLine(trial.get_factor('Word'),
                                text_size=TEXT_SIZE,
                                text_font=TEXT_FONT)
        stim.preload()
        trial.add_stimulus(stim)
    
    if modality == 'Audio':
        audiofile = Path(audio_folder_path) / trial.get_factor('Audio File')
        stim = stimuli.Audio(str(audiofile))
        stim.preload()
        trial.add_stimulus(stim)

    duration = float(trial.get_factor('Trial Duration'))
    new_onset = prev_onset + duration * 1000
    trial.set_factor('target_onset_time', prev_onset)
    prev_onset = new_onset
    #if DEBUG:
    #    print(trial.factors_as_text)

total_duration = prev_onset + FINAL_WAIT
print("Total number of events: ", len(b.trials))
print("Expected Total duration: ", total_duration/1000.0, "s")

######## Instructions ########################################
control.start(skip_ready_screen=True)
    
# Display instructions based on the first row's modalities
input_modality = b.trials[0].get_factor('Input Modality')
output_modality = b.trials[0].get_factor('Output Modality')
display_instructions(input_modality, output_modality, instruction_image_folder)
# Wait for CONTROLLER_KEY
exp.keyboard.wait_char(CONTROLLER_KEY)

stimuli.TextLine('Préparez-vous...').present()
# Wait for trigger signal
exp.keyboard.wait_char(TRIGGER_KEY)

start_time = exp.clock.time

exp.screen.clear()
exp.screen.update()

exp.data.add_experiment_info("Stimfile: " + stim_file)
exp.data.add_variable_names(['modality',
                             'item',
                             'target_timestamp',
                             'actual_timestamp',
                             'key',
                             'rt'])

########### main loop ##############################
end_time = 0
for itrial, t in enumerate(b.trials):
    cue.present()

    target_onset_time = t.get_factor("target_onset_time")
    current_time = exp.clock.time - start_time
    delta = target_onset_time - current_time
    
    duration = float(t.get_factor("Trial Duration")) * 1000        

    while exp.clock.time - start_time < target_onset_time:
        pass
    
    t.stimuli[0].present()
    actual_onset_time = exp.clock.time - start_time
    delta = actual_onset_time - target_onset_time
    
    exp.clock.wait(STIMULUS_DURATION)
    cue.present()

    if delta > 16:
        warn = "!!!"
    else:
        warn = ""

    print(f"{itrial}: Scheduled: {target_onset_time} Actual: {actual_onset_time} delta: {delta}{warn}")

    wait_time = duration - STIMULUS_DURATION - 200 - delta
    key, rt = exp.keyboard.wait_char(RESPONSE_KEY,
                                     duration=wait_time,
                                     process_control_events=True)
    if rt is not None:
        rt = rt + STIMULUS_DURATION
    end_time = exp.clock.time - start_time
    
    exp.data.add([t.get_factor('Input Modality'),
                  t.get_factor('Word'),
                  target_onset_time,
                  actual_onset_time,
                  key,
                  rt])

# wait for FINAL_WAIT before closing
# and record potential TRIGGER timestamps    
while exp.clock.time - start_time < total_duration:
    if exp.keyboard.check(TRIGGER_KEY):
        exp.data.add([exp.clock.time, exp.clock.time,'TRIGGER'])
    pass

control.end()
