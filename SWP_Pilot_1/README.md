# Running the Experiment

# 1. Training
# 438 s total, 1 initial run w/ instructions, 2 runs mimicking main-exp, 88 or 175 s each + instructions (30 sec ?)	

# Run Instructions: 
cd training 

python swp_train_initial.py training_run_1.csv
python swp_train.py training_run_2.csv
python swp_train.py training_run_3.csv

cd .. 

# 2. Main-Exp
# 420 s each run; 42 min total - 5 s before first block,  4 blocks of 90 s w/ 15 s rest, 10 s after final block
# Run Instructions:
cd main-exp

python swp.py sub1_run_1.csv
python swp.py sub1_run_2.csv
python swp.py sub1_run_3.csv
python swp.py sub1_run_4.csv
python swp.py sub1_run_5.csv
python swp.py sub1_run_6.csv


# 3. Localizer (all have 1.5s Merci after)
# Visual 260 s - 6 s before first block, 14 sec per block (8 =20*0.4 s stim + 6 s rest), 8 s after last stim 
# Audio	 196 s - 2 s before first block, 16 s per block (10 s stim + 6 rest), 2 s after last stim	
# Hand	 191 s - 3 s before first, 10 s per block, 6 s rest after, 2 s after last stim	
# Speech 191 s - 3 s before first, 10 s per block, 6 s rest after, 2 after last stim

# Run Instructions: 
cd localizer

python runVisualCategory.py
python audiovis.py --total-duration 196000 audio_categories/sub1_audio.csv
python audiovis.py --splash hand_categories/instructions.png --total-duration 191000 hand_categories/sub1_hand.csv
python audiovis.py --splash speech_categories/instructions.png --total-duration 191000 speech_categories/sub1_speech.csv