import os

def delete_aiff_files(folder_path):
    """
    Deletes all .aiff files in the specified folder.

    Args:
        folder_path (str): Path to the folder containing the files.
    """
    for filename in os.listdir(folder_path):
        # Check if the file has a .aiff extension
        if filename.endswith('.aiff'):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):  # Ensure it's a file, not a folder
                os.remove(file_path)  # Delete the file
                print(f"Deleted: {file_path}")
# Run babee
folder_path = r'C:\Users\ali_a\Desktop\Single_Word_Processing_Stage\Single_Word_Processing\Stimuli\Auditory\English\Mac_MP3_Files'
delete_aiff_files(folder_path)
