# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Main view
import sys
from datetime import datetime
import logging
from PyQt6 import QtWidgets, uic
from app.processing.file_handler import FileHandler
from app.ui.console_handler import ConsoleHandler


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.file_handler = None
        self._selected_file_path = None
        self.select_file_text = None
        self.search_term = None
        uic.loadUi("ui/main_view.ui", self)

        # Configure
        logging.basicConfig(
            filename=f"logs/{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_log.txt",
            level=logging.INFO,
        )

        # Access elements from UI
        self.select_file_button = self.findChild(
            QtWidgets.QPushButton, "select_file_button"
        )
        self.find_text = self.findChild(QtWidgets.QLineEdit, "find_text")
        self.find_button = self.findChild(QtWidgets.QPushButton, "find_button")
        self.preview_element = self.findChild(QtWidgets.QGraphicsView, "preview_frame")
        self.prev_button = self.findChild(QtWidgets.QPushButton, "prev_button")
        self.start_stop_button = self.findChild(
            QtWidgets.QPushButton, "start_stop_button"
        )
        self.next_button = self.findChild(QtWidgets.QPushButton, "next_button")
        self.information_output = self.findChild(
            QtWidgets.QTextEdit, "information_output"
        )
        self.progress_bar = self.findChild(QtWidgets.QProgressBar, "progress_bar")

        # Redirect standard output to console
        sys.stdout = ConsoleHandler(self.information_output)

        # Connect button click event to method
        self.select_file_button.clicked.connect(self.show_file_selector)

    def show_file_selector(self):
        file_dialog = QtWidgets.QFileDialog()
        options = file_dialog.options()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Open File", "/", "Video Files (*.mp4 *.mkv)", options=options
        )

        # Retrieve search term
        if file_path:
            self.select_file_text.setText(file_path.split("/")[-1])
            # Store file path for later use when find button is clicked
            self._selected_file_path = file_path
            # Connect find button if not already connected
            self.find_button.clicked.connect(self.handle_find_button)
        elif not file_path:
            print("No file selected")

    def handle_find_button(self):
        # Get search term
        self.search_term = self.find_text.text()

        # TODO: Here we want to do text analysis

        # Check if file path and search term are set
        if hasattr(self, "_selected_file_path") and self.search_term:
            self.create_file_handler(self._selected_file_path)
        elif not hasattr(self, "_selected_file_path") and not self.search_term:
            print("No file selected or search term provided")
        elif not self.search_term:
            print("No search term provided")
        elif not hasattr(self, "_selected_file_path"):
            print("No file selected")

    def create_file_handler(self, file_path):
        # Create file handler instance and play video
        self.file_handler = FileHandler(
            file_path,
            preview_element=self.preview_element,
            progress_bar=self.progress_bar,
        )
        self.file_handler.extract_keyframes()
