# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Frame display

import cv2
import os
from PyQt6 import QtCore
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QGraphicsScene, QApplication

class FrameDisplayer:
    def __init__(self, preview_element, output_dir='key_frames'):
        self.preview_element = preview_element
        self.output_dir = output_dir
        # Create a scene
        self.scene = QGraphicsScene()

    def display_frame(self, frame_path, frame_count, total_frames):
        image = QImage('key_frames/' + frame_path)
        pixmap = QPixmap.fromImage(image)
        self.scene.addPixmap(pixmap)  # Add pixmap to scene

        self.preview_element.setScene(self.scene)
        self.preview_element.fitInView(self.scene.itemsBoundingRect(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)  # Keep bounds of video
        QApplication.processEvents()
        cv2.waitKey(100) # Temporary delay to display frame

        # Display frame count
        print(f"Processing frame {frame_count} of {total_frames}")

    def display_frames(self):
        # Get list of frame files
        frame_files = os.listdir(self.output_dir)
        frame_files.sort()

        total_frames = len(frame_files)
        frame_count = 1

        # Display each frame in preview window
        for frame_path in frame_files:
            self.display_frame(frame_path, frame_count, total_frames)
            frame_count += 1

        # Set the scene to the preview element
        self.preview_element.setScene(self.scene)