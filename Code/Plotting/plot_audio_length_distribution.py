import os
import wave
import matplotlib

AUDIO_FOLDER_PATH = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Paradigm\Stimuli\Audio_Files_Google_Cloud"
import matplotlib.pyplot as plt

def get_wav_length(file_path):
    with wave.open(file_path, 'r') as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
        return duration

wav_lengths = []
word_lengths = []

for file_name in os.listdir(AUDIO_FOLDER_PATH):
    if file_name.endswith('.wav'):
        file_path = os.path.join(AUDIO_FOLDER_PATH, file_name)
        try:
            wav_length = get_wav_length(file_path)
            word_length = len(file_name.split('_')[0])
            wav_lengths.append(wav_length)
            word_lengths.append(word_length)
        except wave.Error:
            print(f"Error processing {file_path}: file does not start with RIFF id")
        wav_lengths.append(wav_length)
        word_lengths.append(word_length)

plt.scatter(word_lengths, wav_lengths)
plt.xlabel('Length of the Word')
plt.ylabel('Time (seconds)')
plt.title('Distribution of Audio File Lengths')
plt.show()