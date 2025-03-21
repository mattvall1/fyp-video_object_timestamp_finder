# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
"""File handler module for processing video files and extracting keyframes."""

import os
import csv
from app.global_tools import Tools
from app.processing.frame_display import FrameDisplayer
from app.processing.image_captioning_handler import ImageCaptioningHandler
from app.processing.key_framing import KeyFraming


def setup_caption_file(video_name):
    """
    Set up CSV writer for storing captions.

    Parameters:
        video_name: Name of the video file being processed

    Return:
        tuple: CSV writer and file handle
    """
    # Open the CSV file to write results to - DO NOT use 'with' statement (as it closes the file)
    captions_file = open(
        f"data/data_files/{video_name}_captions.csv",
        "w",
        newline="\n",
        encoding="utf-8",
    ) # pylint: disable=consider-using-with
    csv_writer = csv.writer(captions_file)
    return csv_writer, captions_file


class FileHandler:
    """Handles video file processing, keyframe extraction, and caption generation."""

    def __init__(self, file_path, element_handler):
        self.file_path = file_path
        self.element_handler = element_handler
        self.frame_displayer = FrameDisplayer(self.element_handler.preview_element)
        self.progress_bar = self.element_handler.progress_bar
        self.output_dir = "data/key_frames"

        # Delete old frames
        Tools.clear_frame_directories()

        # Create writer for caption file
        self.csv_writer, self.results_file = setup_caption_file(
            file_path.split(".")[0].split("/")[-1]
        )

    def extract_keyframes(self):
        """Extract keyframes from the video file and process them."""
        # Create instance of KeyFraming
        key_fr = KeyFraming(
            file_path=self.file_path,
            output_dir=self.output_dir,
            frame_displayer=self.frame_displayer,
            progress_bar=self.progress_bar,
        )
        key_fr.extract_keyframes()

        # Generate captions for keyframes
        self.process_keyframes()

    def process_keyframes(self):
        """Process extracted keyframes by generating and analyzing captions."""
        # Create instance of ImageCaptioningHandler
        frame_caption_generator = ImageCaptioningHandler(
            original_output_dir=self.output_dir
        )

        # Get list of frames sorted alphabetically, and get total frames
        frames_path_list = sorted(os.listdir(self.output_dir))
        total_frames = len(frames_path_list)

        # Loop through frames and detect objects
        frame_count = 1
        for frame in frames_path_list:
            print(f"Processing frame {frame_count} of {total_frames}")

            # Caption frame
            generator_output = frame_caption_generator.frame_caption(frame)
            print("Generated caption: " + generator_output[1])

            # Display frame in preview window
            self.frame_displayer.display_frame(generator_output[0])

            # Compare caption to search term
            search_results = (
                self.element_handler.search_term_handler.compare_caption_to_search_term(
                    generator_output[1]
                )
            )
            # TEMP PRINT
            if search_results:
                print(f"Search term found: {", ".join(search_results)}")
                print("PAUSE SIGNAL")
                # Pause processing

            else:
                print("Search term not found")

            # Save caption to CSV
            self.save_caption(frame, generator_output[1])

            # Update progress bar (second half of bar)
            self.progress_bar.setValue(50 + int((frame_count / total_frames) * 50))
            frame_count += 1

        # Close the CSV file after writing all captions
        self.results_file.close()

    def save_caption(self, frame, caption):
        """
        Save the caption to the CSV file.

        Parameters:
            frame: Frame identifier
            caption: Generated caption text
        """
        # Save the caption to a text file, using the writer created earlier
        self.csv_writer.writerow([frame, caption])
        print("Caption saved for frame")
