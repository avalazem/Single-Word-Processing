import os
from pydub import AudioSegment

# Path to the folder containing the .wav files
input_folder = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\Stimuli\audio_files_wav"
output_folder = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\Stimuli\reversed_audio_files_wav"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Process each .wav file in the input folder
for file_name in os.listdir(input_folder):
    if file_name.endswith(".wav"):  # Only process .wav files
        file_path = os.path.join(input_folder, file_name)

        # Load the audio file
        audio = AudioSegment.from_wav(file_path)
        
        # Reverse the audio
        reversed_audio = audio.reverse()
        
        # Save the reversed audio to the output folder
        output_path = os.path.join(output_folder, f"rvrs_{file_name}")
        reversed_audio.export(output_path, format="wav")
        print(f"Reversed and saved: {output_path}")

print("All files have been processed!")
