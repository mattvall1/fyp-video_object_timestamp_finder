# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Frame display

import cv2
import os
from PyQt6 import QtCore
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QGraphicsScene, QApplication

class FrameDisplayer:
    def __init__(self, preview_element, frame_counter, output_dir='key_frames'):
        self.preview_element = preview_element
        self.frame_counter = frame_counter
        self.output_dir = output_dir

    def display_frames(self):
        # Get list of frame files
        frame_files = os.listdir(self.output_dir)
        frame_files.sort()

        scene = QGraphicsScene()  # Create a scene
        frame_count = 1
        # Display each frame in preview window
        for frame_path in frame_files:
            image = QImage('key_frames/' + frame_path)
            pixmap = QPixmap.fromImage(image)
            scene.addPixmap(pixmap)  # Add pixmap to scene

            self.preview_element.setScene(scene)
            self.preview_element.fitInView(scene.itemsBoundingRect(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)  # Keep bounds of video
            QApplication.processEvents()
            cv2.waitKey(100)

            # Display frame count
            self.frame_counter.setText(f"Processing frame {frame_count} of {len(frame_files)}")
            frame_count += 1

        # Set the scene to the preview element
        self.preview_element.setScene(scene)