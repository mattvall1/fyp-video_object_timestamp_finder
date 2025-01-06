# Script to delete all key frames from the key_frames directory
import os

class Tools:
    @staticmethod
    def clear_key_frames():
        directory = 'key_frames'
        count = 0
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
                count += 1
        print(f"Deleted {count} files")