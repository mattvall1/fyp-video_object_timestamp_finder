# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Katna library testing for key framing (Based upon quickstart)
from Katna.video import Video
from Katna.writer import KeyFrameDiskWriter

def get_keyframes():
    # Instantiate the video object
    vid = Video()

    # Settings
    output_dir = "key_frames_katna"
    video_path = "../../testing_videos/highway_driving.mp4"
    total_frames_to_retrieve = 10

    # initialize diskwriter to save data at desired location
    diskwriter = KeyFrameDiskWriter(location=output_dir)

    # Extract keyframes and process data
    vid.extract_video_keyframes(
        no_of_frames=total_frames_to_retrieve, file_path=video_path,
        writer=diskwriter
    )

if __name__ == "__main__":
    get_keyframes()