# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: FFmpeg key frame extraction using ffmpeg-python
import ffmpeg
from pathlib import Path


def get_keyframes_ffmpeg():
    # Settings
    video_path = "../../testing_videos/highway_driving.mp4"
    output_dir = "outputs/key_frames_ffmpeg"
    total_frames_to_retrieve = 10

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Define output pattern
    output_pattern = f"{output_dir}/keyframe_%04d.jpg"

    # ffmpeg filter complex
    (
        ffmpeg.input(video_path)
        .filter("select", "eq(pict_type,I)")
        .output(
            output_pattern,
            vsync="vfr",
            q=0,  # Quality scale - 0 is lossless, we want minimal performance loss, compression is not a concern
            vframes=total_frames_to_retrieve,
        )
        .overwrite_output()
        .run()
    )

    print(f"Keyframes extracted to {output_dir}")


if __name__ == "__main__":
    get_keyframes_ffmpeg()
