# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Script theory of binary search (effectively the first draft)
# Note: This will only work if we know FOR DEFINITE that there is a specific object in the video - that is okay.
# Imports
import os
from frame_searching_azure import FrameSearcher

# Get list of all images in frames dir
total_frames = len(os.listdir('frames'))

# Get subset of frames to search (every 60th frame)
initial_subset = []
for frame in range(1800, total_frames, 60):
    initial_subset.append(f'{frame:04d}')

# Check each image in initial subset
for frame in initial_subset:
    frame_search = FrameSearcher()

    image = frame_search.get_image(image_path=f"frames/{frame}.jpg")
    # Ignore first caption, as that encompasses the whole image
    captions = frame_search.get_captions(image=image)[1:]
    print(f"frames/{frame}.jpg", captions)

