import random
import pandas as pd
from pathlib import Path

def create_visual_cat_localizer(SUBJECT):
    csv_path = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Localizer\Stimuli\CSVs"
    
    block_reps=3
    INTERBLOCK_DURATION = 6000  # in ms
    STIM_DURATION = 100
    ONSET = 2000
    categories=['face', 'emoji', 'wordEF', 'wordEF', 'wordC', 'Mu']

    shuffled_categories = []
    localizer = []
    
    for _ in range(block_reps):
        temp = categories[:]
        random.shuffle(temp)
        # Ensure no consecutive repetitions between blocks
        while len(shuffled_categories) > 0 and shuffled_categories[-1] == temp[0]:
            random.shuffle(temp)
        # Ensure no consecutive repetitions within the block
        while any(temp[i] == temp[i + 1] for i in range(len(temp) - 1)):
            random.shuffle(temp)
        shuffled_categories.extend(temp)

    categories = shuffled_categories

    has_star = ([1] * len(categories)) + ([0] * len(categories) * (block_reps - 1))
    random.shuffle(has_star)

    stims_idx = [x + 1 for x in range(20)]
    onset = ONSET

    first_block = True
    for bloc_type in zip(categories, has_star):
        random.shuffle(stims_idx)
        stims = [f"{bloc_type[0]}{x:02}.png" for x in stims_idx]
        if bloc_type[1] == 1:   # add star
            pos = random.choice(range(1, len(stims)))
            stims[pos] = "star.png"
        if not first_block:
            onset += INTERBLOCK_DURATION - STIM_DURATION # adjusting for onset
        first_block = False
        for x in stims:
            localizer.append((onset, 'picture', x))
            #print((onset, x))
            onset += STIM_DURATION

    # Convert the localizer list to a Pandas DataFrame
    df = pd.DataFrame(localizer, columns=['onset', 'type', 'stim'])

    # Save the DataFrame to a CSV file
    df.to_csv(Path(csv_path) / f"{SUBJECT}_vis.csv", index=False)
    print("Localizer CSV file created successfully.")

#create_visual_cat_localizer('sub1')