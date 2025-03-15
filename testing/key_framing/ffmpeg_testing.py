# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: FFmpeg key frame extraction
import os
import subprocess
import ffmpeg
import cv2
from pathlib import Path


def get_keyframes_ffmpeg():
    # Settings
    video_path = "../../testing_videos/highway_driving.mp4"
    output_dir = "outputs/key_frames_ffmpeg"
    total_frames_to_retrieve = 10

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Get video info using ffprobe
    probe = ffmpeg.probe(video_path)
    video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    duration = float(video_info['duration'])

    # First approach: Extract I-frames using ffmpeg
    # Generate a command to identify keyframes
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-vf', 'select=eq(pict_type\\,I)',
        '-vsync', 'vfr',
        '-vframes', str(total_frames_to_retrieve),
        '-q:v', '2',
        '-f', 'image2',
        f'{output_dir}/keyframe_%04d.jpg'
    ]

    # Run the command
    subprocess.run(cmd)
    print(f"Keyframes extracted to {output_dir}")

if __name__ == "__main__":
    get_keyframes_ffmpeg()