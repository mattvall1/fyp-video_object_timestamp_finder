# Script to delete all key frames from the key_frames directory
import os


class Tools:
    @staticmethod
    def clear_frame_directories():
        directories = ["data/key_frames", "data/data_files"]
        count = 0
        for directory in directories:
            for file_name in os.listdir(directory):
                file_path = os.path.join(directory, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    count += 1
        print(f"Deleted {count} files")

    @staticmethod
    def create_directories():
        directories = ["data", "data/data_files", "data/key_frames", "logs"]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")
