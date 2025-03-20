# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Main view
import sys
from datetime import datetime
import logging
from PyQt6 import QtWidgets, uic
from app.processing.file_handler import FileHandler
from app.ui.console_handler import ConsoleHandler
from app.ui.button_handler import ButtonHandler


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.file_handler = None
        self._selected_file_path = None
        self.search_term_handler = None
        uic.loadUi("ui/main_view.ui", self)

        # Configure
        logging.basicConfig(
            filename=f"logs/{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_log.txt",
            level=logging.INFO,
        )
        
        # Initialize button handler
        self.button_handler = ButtonHandler(self)
        
        # Redirect standard output to console
        sys.stdout = ConsoleHandler(self.button_handler.information_output)

    def create_file_handler(self):
        # Create file handler instance and play video
        self.file_handler = FileHandler(
            self._selected_file_path,
            preview_element=self.button_handler.preview_element,
            search_term_handler=self.search_term_handler,
            progress_bar=self.button_handler.progress_bar,
        )
        self.file_handler.extract_keyframes()


