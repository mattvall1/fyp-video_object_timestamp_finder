import os
import cv2
from pathlib import Path

def extract_thumbnail(video_path, output_dir):
    """
    Extract the middle frame from a video and save it as a JPEG thumbnail.
    
    Args:
        video_path: Path to the video file
        output_dir: Directory to save the thumbnail
    """
    # Create video capture object
    video = cv2.VideoCapture(str(video_path))
    
    # Check if video opened successfully
    if not video.isOpened():
        print(f"Error: Could not open video {video_path}")
        return
    
    # Get total number of frames
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if total_frames <= 0:
        print(f"Error: Could not determine frame count for {video_path}")
        return
    
    # Set position to middle frame
    middle_frame_idx = total_frames // 2
    video.set(cv2.CAP_PROP_POS_FRAMES, middle_frame_idx)
    
    # Read the frame
    success, frame = video.read()
    
    if not success:
        print(f"Error: Could not read middle frame from {video_path}")
        return
    
    # Create thumbnail filename with same name as video but jpg extension
    thumbnail_path = output_dir / f"{video_path.stem}.jpg"
    
    # Save the frame as JPEG
    cv2.imwrite(str(thumbnail_path), frame)
    print(f"Created thumbnail: {thumbnail_path}")
    
    # Release video object
    video.release()

def main():
    # Get current directory
    current_dir = Path(__file__).parent
    
    # Create thumbnails directory if it doesn't exist
    thumbnails_dir = current_dir / "thumbnails"
    thumbnails_dir.mkdir(exist_ok=True)
    
    # Process all video files
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
    
    for file_path in current_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in video_extensions:
            print(f"Processing video: {file_path}")
            extract_thumbnail(file_path, thumbnails_dir)

if __name__ == "__main__":
    main()