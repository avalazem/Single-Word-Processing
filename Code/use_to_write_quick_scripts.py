from gtts import gTTS
import os

# Text to be converted to speech
text = "press"

# Create a gTTS object
tts = gTTS(text=text, lang='en')

# Save the audio file
output_path = r'C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\audio_files_wav\press.wav'
tts.save(output_path)

# Convert mp3 to wav using pydub
from pydub import AudioSegment

# Load the mp3 file
audio = AudioSegment.from_mp3(output_path)

# Export as wav
audio.export(output_path, format="wav")

print(f"Audio file saved at {output_path}")