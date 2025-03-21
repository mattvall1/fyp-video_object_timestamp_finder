# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
"""
Key framing module for extracting significant frames from videos.
Based on: https://www.ijeast.com/papers/51-56,Tesma108,IJEAST.pdf
"""
import os
import shutil

import cv2
import matplotlib.pyplot as plt

# TODO: Mention in report here we started with katna but it didnt do what I wanted


class KeyFraming:
    # pylint: disable=too-few-public-methods
    """Handles the extraction of key frames from video files by using S Ghatak's method."""

    def __init__(self, file_path, output_dir, frame_displayer, progress_bar):
        self.file_path = file_path
        self.output_dir = output_dir
        self.frame_displayer = frame_displayer
        self.progress_bar = progress_bar

        # Split video method
        self.total_frames = 0
        self.all_frames = "data/original_frames"

    # Module 1 - Extract all original frames
    def _split_video(self):
        # Open video file
        video_cap = cv2.VideoCapture(self.file_path)
        if not video_cap.isOpened():
            print(f"Error: Could not open video file {self.file_path}")
            return

        success, image = video_cap.read()
        if not success:
            print("Error: Could not read video")
            video_cap.release()
            return

        self.total_frames = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        count = 0

        while success:
            # Save frame as JPEG file
            frame_path = os.path.join(self.all_frames, f"{count:04d}.jpg")
            cv2.imwrite(frame_path, image)
            success, image = video_cap.read()
            print(f"Saving frame '{frame_path}'")

            # Display frame
            self.frame_displayer.display_frame(frame_path)

            # Update progress bar (first third of first half of bar)
            self.progress_bar.setValue(int((count / self.total_frames) * 16))

            count += 1

        video_cap.release()

    # Module 2 - Calculate frame differences
    def _calculate_frame_difference(self):
        # Read all frames from the directory
        frames = sorted(os.listdir(self.all_frames))
        frame_diffs = []

        # Clear frame displayer (fixes resolution issues)
        self.frame_displayer.clear_frame()

        for i in range(len(frames) - 1):
            print(
                f"Calculating frame difference for frame {frames[i]} and frame {frames[i + 1]}..."
            )
            # Create array to hold frame differences
            frame_diff = [frames[i], frames[i + 1]]

            # Retrive frames
            frame_1_path = os.path.join(self.all_frames, frames[i])
            frame_2_path = os.path.join(self.all_frames, frames[i + 1])

            # Read two consecutive frames
            frame_1 = cv2.imread(frame_1_path)
            frame_2 = cv2.imread(frame_2_path)

            # Convert frames to grayscale
            frame_1_gray = cv2.cvtColor(frame_1, cv2.COLOR_BGR2GRAY)
            frame_2_gray = cv2.cvtColor(frame_2, cv2.COLOR_BGR2GRAY)

            # Generate histograms
            frame_1_hist, frame_2_hist = self._generate_histograms(
                frame_1_gray, frame_2_gray
            )

            # Find difference of the two frames
            difference = cv2.absdiff(frame_1_hist, frame_2_hist)
            frame_diff.append(difference)

            # Calculate the sum of the absolute differences
            sum_diff = cv2.sumElems(difference)[0]
            frame_diff.append(sum_diff)
            print(f"Absolute difference: {sum_diff}")

            # Plot histograms
            self._plot_histogram(
                frame_1_gray,
                frame_2_gray,
                frame_1_hist,
                frame_2_hist,
                frame_1_path,
                frame_2_path,
            )

            # Add this frame difference to main list
            frame_diffs.append(frame_diff)

            # Update progress bar (second third of first half of bar)
            self.progress_bar.setValue(16 + int((i / len(frames)) * 16))

        return frame_diffs

    # Module 2 - Generate histograms
    @staticmethod
    def _generate_histograms(frame_1_gray, frame_2_gray):
        # Calculate histograms (and flatten them)
        hist_1 = cv2.calcHist([frame_1_gray], [0], None, [256], [0, 256]).flatten()
        hist_2 = cv2.calcHist([frame_2_gray], [0], None, [256], [0, 256]).flatten()

        return hist_1, hist_2

    # Module 3 - Calculate threshold  TODO: This is slightly different to the paper, this should run within the loop, but this makes more sense
    @staticmethod
    def _calculate_threshold(frame_diffs, const):
        # Get the mean of the differences
        total_diffs = sum(frame_diff[3] for frame_diff in frame_diffs)
        mean_diffs = total_diffs / len(frame_diffs)

        # Get the standard deviation of the differences TODO: Explain why we do this
        sd_diffs = (
            sum((frame_diff[3] - mean_diffs) ** 2 for frame_diff in frame_diffs)
            / len(frame_diffs)
        ) ** 0.5

        # Find the threshold
        return sd_diffs + (mean_diffs * const)

    # Display histograms from Module 2
    def _plot_histogram(
        self,
        frame_1_gray,
        frame_2_gray,
        frame_1_hist,
        frame_2_hist,
        frame_1_path,
        frame_2_path,
    ):
        # Create figure for plotting (so it fits nicely in the window - 16:9/1080p)
        plt.figure(figsize=(19.2, 10.8), dpi=100)

        # Plot frame 1 and its histogram
        plt.subplot(2, 2, 1)
        plt.imshow(frame_1_gray, cmap="gray")
        plt.title("Frame 1 (Grayscale)")
        plt.axis("off")

        plt.subplot(2, 2, 3)
        plt.bar(range(256), frame_1_hist, color="blue", alpha=0.7)
        plt.title("Histogram")
        plt.xlabel("Pixel Value")
        plt.ylabel("Frequency")

        # Plot frame 2 and its histogram
        plt.subplot(2, 2, 2)
        plt.imshow(frame_2_gray, cmap="gray")
        plt.title("Frame 2 (Grayscale)")
        plt.axis("off")

        plt.subplot(2, 2, 4)
        plt.bar(range(256), frame_2_hist, color="blue", alpha=0.7)
        plt.title("Histogram")
        plt.xlabel("Pixel Value")
        plt.ylabel("Frequency")

        plt.tight_layout()

        # Generate filename based on the frame paths
        frame1_num = os.path.basename(frame_1_path).split(".")[0]
        frame2_num = os.path.basename(frame_2_path).split(".")[0]
        hist_output_path = os.path.join(
            "data/frame_histograms", f"hist_{frame1_num}_{frame2_num}.jpg"
        )

        # Save figure and close
        plt.savefig(hist_output_path, dpi=100)
        plt.close()

        # Display histograms in preview window
        self.frame_displayer.display_frame(hist_output_path)

    def extract_keyframes(self):
        """Complete workflow for extracting keyframes from a video."""
        print("Extracting keyframes...")
        # Module 1 - Extract frames
        self._split_video()

        # Module 2 - Calculate frame differences
        frame_differences = self._calculate_frame_difference()

        # Module 3 - Extract keyframes - CONST VALUE: Smaller const = lower threshold (and vice versa)
        threshold = self._calculate_threshold(frame_differences, 0.7)

        # Module 3 - Loop through frame differences, extract keyframes - copy to keyframes directory
        count = 0
        for frame_diff in frame_differences:
            # Check if the average difference is greater than the threshold
            if frame_diff[3] > threshold:
                selected_keyframe = frame_diff[0]
                print(
                    f"Keyframe found: {selected_keyframe} with difference {frame_diff[3]}..."
                )
                # Move keyframe to output directory
                shutil.move(
                    os.path.join(self.all_frames, selected_keyframe), self.output_dir
                )

            # Update progress bar (last third of first half of bar)
            self.progress_bar.setValue(32 + int((count / self.total_frames) * 16))
            count += 1
