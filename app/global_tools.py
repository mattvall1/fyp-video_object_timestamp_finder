# Script to delete all key frames from the key_frames directory
import os

class Tools:
    @staticmethod
    def clear_frame_directories():
        directories = ['key_frames/objects', 'key_frames/original']
        count = 0
        for directory in directories:
            for file_name in os.listdir(directory):
                file_path = os.path.join(directory, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    count += 1
        print(f"Deleted {count} files")

    @staticmethod
    def create_frame_directories():
        directories = ['key_frames/objects', 'key_frames/original']
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        print("Created directories")