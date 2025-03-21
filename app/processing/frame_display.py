# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
"""Frame display module for rendering frames in the UI."""

from PyQt6 import QtCore
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QGraphicsScene, QApplication


class FrameDisplayer:
    """Handles displaying frames in the application UI using QGraphicsScene."""

    def __init__(self, preview_element):
        self.preview_element = preview_element
        # Create a scene
        self.scene = QGraphicsScene()

    def display_frame(self, frame_path):
        """
        Display a frame in the UI preview element.

        Parameters:
            frame_path: Path to the image file to display
        """
        image = QImage(frame_path)
        pixmap = QPixmap.fromImage(image)
        self.scene.addPixmap(pixmap)  # Add pixmap to scene

        self.preview_element.setScene(self.scene)
        self.preview_element.fitInView(
            self.scene.itemsBoundingRect(), QtCore.Qt.AspectRatioMode.KeepAspectRatio
        )  # Keep bounds of video
        QApplication.processEvents()  # Process events to update UI

    def clear_frame(self):
        """Clear the current frame from the scene and create a new scene."""
        # Clear the scene
        self.scene.clear()

        # Create a new scene
        self.scene = QGraphicsScene()
