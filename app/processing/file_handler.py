# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: File handler
import cv2
import os

from PyQt6 import QtCore
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QGraphicsScene, QApplication
from app.global_tools import Tools

class ImageHandler:

    def __init__(self, file_path, preview_element, frame_counter):
        self.file_path = file_path
        self.preview_element = preview_element
        self.frame_counter = frame_counter
        self.output_dir = 'key_frames'

        # Delete old frames
        Tools.clear_key_frames()


    # Method to split video into frames
    def split_video(self):
        # Open video file
        video_cap = cv2.VideoCapture(self.file_path)
        success, image = video_cap.read()
        count = 0

        while success:
            if count < 50: # Limit to 50 frames (for testing)
                # Save frame as JPEG file
                frame_path = os.path.join(self.output_dir, f"{count:04d}.jpg")
                cv2.imwrite(frame_path, image)
                success, image = video_cap.read()
                print(f"Frame '{frame_path}' saved")
                count += 1
            else:
                break

        video_cap.release()

        # Display frames
        self.display_frames()

    def display_frames(self):
        # Get list of frame files
        frame_files = os.listdir(self.output_dir)
        frame_files.sort()

        scene = QGraphicsScene()  # Create a scene
        # Display each frame in preview window
        for frame_path in frame_files:
            image = QImage('key_frames/'+frame_path)
            pixmap = QPixmap.fromImage(image)
            scene.addPixmap(pixmap)  # Add pixmap to scene

            self.preview_element.setScene(scene)
            self.preview_element.fitInView(scene.itemsBoundingRect(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            QApplication.processEvents()
            cv2.waitKey(100)

        # Set the scene to the preview element
        self.preview_element.setScene(scene)
        self.preview_element.fitInView(scene.itemsBoundingRect(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)


