# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Frame display

from PyQt6 import QtCore
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QGraphicsScene, QApplication


class FrameDisplayer:
    def __init__(self, preview_element):
        self.preview_element = preview_element
        # Create a scene
        self.scene = QGraphicsScene()

    def display_frame(self, frame_path):
        image = QImage(frame_path)
        pixmap = QPixmap.fromImage(image)
        self.scene.addPixmap(pixmap)  # Add pixmap to scene

        self.preview_element.setScene(self.scene)
        self.preview_element.fitInView(
            self.scene.itemsBoundingRect(), QtCore.Qt.AspectRatioMode.KeepAspectRatio
        )  # Keep bounds of video
        QApplication.processEvents()  # Process events to update UI

    def clear_frame(self):
        # Clear the scene
        self.scene.clear()

        # Create a new scene
        self.scene = QGraphicsScene()
