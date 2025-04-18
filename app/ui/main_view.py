# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
"""Main view module for the application UI."""

import sys
from datetime import datetime
import logging
from PyQt6 import QtWidgets, uic
from app.processing.file_handler import FileHandler
from app.ui.console_handler import ConsoleHandler
from app.ui.element_handler import ElementHandler


class MainWindow(QtWidgets.QMainWindow):
    # pylint: disable=too-few-public-methods
    """Handles UI initialization and file processing."""

    def __init__(self):
        super().__init__()
        self.selected_file_path = None
        uic.loadUi("ui/main_view.ui", self)

        # Configure
        logging.basicConfig(
            filename=f"logs/{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_log.txt",
            level=logging.INFO,
        )

        # Initialize button handler
        self.element_handler = ElementHandler(self)

        # Redirect standard output to console
        sys.stdout = ConsoleHandler(self.element_handler.information_output)

    def create_file_handler(self):
        """Create file handler and begin keyframe extraction process."""
        # Create file handler instance and play video
        file_handler = FileHandler(
            self.selected_file_path,
            element_handler=self.element_handler,
        )
        file_handler.retrieve_keyframes()
