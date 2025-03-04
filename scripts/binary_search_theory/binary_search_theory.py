# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Script theory of binary search (effectively the first draft)
# Note: This will only work if we know FOR DEFINITE that there is a specific object in the video - that is okay.
# Imports
import os
import multiprocessing
from frame_searching_florence import FrameSearcher
from caption_processing import CaptionProcessor


def main():
    # Get list of all images in frames dir
    total_frames = len(os.listdir("frames"))

    # Get subset of frames to search (every 60th frame)
    initial_subset = []
    for frame in range(0, total_frames, 60):
        initial_subset.append(f"{frame:04d}")

    # Create frame and caption searcher once
    frame_search = FrameSearcher()
    caption_processor = CaptionProcessor()

    # Check each image in initial subset
    for frame in initial_subset:
        image = frame_search.get_image(image_path=f"frames/{frame}.jpg")
        # Get caption
        caption = frame_search.get_caption(image=image)
        print(f"frames/{frame}.jpg - Caption: {caption}")

        # Get key phrases from caption
        key_phrases = caption_processor.extract_key_phrases(caption)
        print(f"frames/{frame}.jpg - Key phrases: {key_phrases}")


if __name__ == "__main__":
    # This fixes the multiprocessing issue
    multiprocessing.set_start_method("spawn")
    main()
