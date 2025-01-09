import os
import subprocess

# Specify the folder containing .mp3 files
input_folder = r"C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Christophe_Stimulation\Mac_MP3_Files"
output_format = "wav"  # Change to "ogg" if needed

# Ensure the output folder exists
output_folder = os.path.join(input_folder, "converted_files")
os.makedirs(output_folder, exist_ok=True)

# Loop through all .mp3 files in the folder
for filename in os.listdir(input_folder):
    if filename.endswith(".mp3"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + f".{output_format}")
        
        # Run the ffmpeg command
        ffmpeg_command = ["ffmpeg", "-i", input_path, output_path]
        subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Converted: {input_path} -> {output_path}")

print("Conversion completed!")
