# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: File handler module for processing video files and extracting keyframes.

import os
import csv
import time

from app.global_tools import Tools
from app.processing.completion_handler import CompletionHandler
from app.processing.frame_display import FrameDisplayer
from app.processing.image_captioning_handler import ImageCaptioningHandler
from app.processing.key_frame_handler import KeyFrameHandler

class FileHandler:
    """Handles video file processing, keyframe extraction, and caption generation."""

    def __init__(self, file_path, element_handler):
        self.file_path = file_path
        self.element_handler = element_handler
        self.frame_displayer = FrameDisplayer(self.element_handler.preview_element)
        self.progress_bar = self.element_handler.progress_bar
        self.output_dir = "data/key_frames"
        self.matching_frames = []

        # Delete old frames
        Tools.clear_frame_directories()

        # Create writer for caption file
        self.csv_writer, self.results_file = self._setup_caption_file(
            file_path.split(".")[0].split("/")[-1]
        )

    @staticmethod
    def _setup_caption_file(video_name):
        """
        Set up CSV writer for storing captions.

        Parameters:
            video_name: Name of the video file being processed

        Return:
            tuple: CSV writer and file handle
        """
        # Open the CSV file to write results to - DO NOT use 'with' statement (as it closes the file)
        # pylint: disable=consider-using-with
        captions_file = open(
            f"data/{video_name}_captions.csv",
            "w",
            newline="\n",
            encoding="utf-8",
        )
        csv_writer = csv.writer(captions_file)
        return csv_writer, captions_file

    def retrieve_keyframes(self):
        """Extract keyframes from the video file and process them."""
        # Create instance of KeyFraming
        key_fr = KeyFrameHandler(
            file_path=self.file_path,
            output_dir=self.output_dir,
            frame_displayer=self.frame_displayer,
            progress_bar=self.progress_bar,
        )
        key_fr.extract_keyframes()

        # Generate captions for keyframes
        self._process_keyframes()

    def _process_keyframes(self):
        """This is the main processing function. It handles the captioning of keyframes etc."""
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
            print("Generated caption: " + generator_output)

            # Display frame in preview window
            self.frame_displayer.display_frame(self.output_dir + "/" + frame)

            # Compare caption to search term
            search_results = (
                self.element_handler.search_term_handler.compare_caption_to_search_term(
                    generator_output
                )
            )

            # Save caption to CSV
            self.save_caption(frame, generator_output)

            if search_results:
                # Get timestamp for the frame - divide by 1000 to convert to seconds
                timestamp = int(frame.split("_")[1].split(".")[0]) / 1000

                # Add frame to matching frames list (we need to save the path to the frame here)
                self.matching_frames.append({"filename": self.output_dir + "/" + frame, "caption": generator_output, "timestamp": timestamp})

                # Print search results
                print(
                    f"Search term found: {", ".join(search_results)} at {timestamp} seconds"
                )

                # Pause processing (continue regardless of user input after 10 seconds)
                self.element_handler.handle_continue_button()
                ignore_wait_seconds = 10
                while self.element_handler.continue_button.isEnabled() and ignore_wait_seconds != 0:
                    print(f"Processing paused, press continue to resume. Continuing in {ignore_wait_seconds} seconds")
                    time.sleep(1)
                    ignore_wait_seconds -= 1
                print("Processing resumed")

            else:
                print("Search term not found")

            # Update progress bar (second half of bar)
            self.progress_bar.setValue(50 + int((frame_count / total_frames) * 50))
            frame_count += 1

        # Close the CSV file after writing all captions
        self.results_file.close()
        print("All captions saved to CSV file.")

        # Run completion handler
        completion_handler = CompletionHandler(self.element_handler, self.matching_frames)
        # Ask user if they want to generate a report

        generate_report = self.element_handler.generate_report_modal()
        if generate_report:
            completion_handler.generate_completion_report(generate_report)

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
