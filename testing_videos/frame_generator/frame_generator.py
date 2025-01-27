# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: This script generates simple frames that can be used to test video processing algorithms
# Caution: This script generates a large number of frames, don't run it unless you need to
# Note: Remember to use the .run configuration to run this script, as it requires some exports to be set
import svgwrite
from pathlib import Path
import shutil
import cairosvg

def generate_frame(object_position: tuple, frame_num: int):
    # Set up the SVG frame
    frame = svgwrite.Drawing(f'temp_svg/{frame_num}.svg', profile='tiny', size=(1920, 1080))

    # Add circle
    frame.add(frame.circle(center=object_position, r=250, fill='red'))

    # Save the frame
    frame.save()

# First, clean and setup directories
try:
    shutil.rmtree(Path('red_ball_frames')) # Delete red_ball_frames directory
except FileNotFoundError:
    pass # We don't need to do anything in this case

Path('red_ball_frames').mkdir(parents=True, exist_ok=True) # Delete and create red_ball_frames directory
Path('temp_svg').mkdir(parents=True, exist_ok=True) # Create temp_svg directory if it doesn't exist

# Next, generate all frames
total_frames = 2420 # Note: with a value of 2420, the object will move the entire way across the screen
for frame in range(total_frames):
    print(f'Generating frame {frame}')
    generate_frame((frame-250, 500), frame)

# Then, convert all SVG frames to PNG
for svg_frame in sorted(Path('temp_svg').iterdir(), key=lambda x: int(x.stem)):
    # Convert SVG to PNG
    print(f'Converting {svg_frame} to PNG')
    cairosvg.svg2png(url=str(svg_frame), write_to=str(f'red_ball_frames/{svg_frame.stem}.png'))


# Finally, delete temporary SVG frame directory
shutil.rmtree(Path('temp_svg'))
print('Done')

