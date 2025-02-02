# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: This script takes the output of the frame_generator script and creates a video from the frames
# Note: ffmpeg must be installed on your system to run this script
import os
import subprocess


# List all PNG files in the directory
png_files = sorted([f for f in os.listdir('red_ball_frames') if f.endswith('.png')])

# Construct the ffmpeg command
ffmpeg_command = [
    'ffmpeg',
    '-framerate', '30',
    '-i', 'red_ball_frames/%d.png',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-crf', '0',
    '../red_ball.mp4'
]

# Run the ffmpeg command
subprocess.run(ffmpeg_command, check=True)