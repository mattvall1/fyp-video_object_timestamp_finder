# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Tools to delete and create directories
import os

class Tools:
    @staticmethod
    def clear_frame_directories():
        directories = [
            "data/key_frames",
            "data/original_frames",
            "data/frame_histograms",
        ]
        count = 0
        for directory in directories:
            for file_name in os.listdir(directory):
                file_path = os.path.join(directory, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    count += 1

        return count

    @staticmethod
    def create_directories():
        directories = [
            "data",
            "data/key_frames",
            "data/frame_histograms",
            "data/original_frames",
            "logs",
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")
