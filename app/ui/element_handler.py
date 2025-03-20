# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Button handling functionality

from PyQt6 import QtWidgets
from app.processing.language_handler import LanguageHandler

class ElementHandler:
    def __init__(self, main_window):
        # Get reference to the main window
        self.main_window = main_window
        self._selected_file_path = None
        self.search_term_handler = None
        
        # Find all UI elements
        self.select_file_button = self.main_window.findChild(QtWidgets.QPushButton, "select_file_button")
        self.select_file_text = self.main_window.findChild(QtWidgets.QLineEdit, "select_file_text")
        self.find_text = self.main_window.findChild(QtWidgets.QLineEdit, "find_text")
        self.find_button = self.main_window.findChild(QtWidgets.QPushButton, "find_button")

        self.preview_element = self.main_window.findChild(QtWidgets.QGraphicsView, "preview_frame")

        self.prev_button = self.main_window.findChild(QtWidgets.QPushButton, "prev_button")
        self.start_stop_button = self.main_window.findChild(QtWidgets.QPushButton, "start_stop_button")
        self.next_button = self.main_window.findChild(QtWidgets.QPushButton, "next_button")

        self.progress_bar = self.main_window.findChild(QtWidgets.QProgressBar, "progress_bar")
        self.information_output = self.main_window.findChild(QtWidgets.QTextEdit, "information_output")
        
        # Connect button click events to methods
        self.connect_buttons()
    
    def connect_buttons(self):
        # Connect the select file button to the file selector
        self.select_file_button.clicked.connect(self.show_file_selector)

        # Connect the find button to the find handler
        self.find_button.clicked.connect(self.handle_find_button)
    
    def show_file_selector(self):
        file_dialog = QtWidgets.QFileDialog()
        options = file_dialog.options()
        file_path, _ = file_dialog.getOpenFileName(
            self.main_window, "Open File", "/", "Video Files (*.mp4 *.mkv)", options=options
        )

        # Retrieve search term
        if file_path:
            self.select_file_text.setText(file_path.split("/")[-1])
            # Store file path for later use when find button is clicked
            self._selected_file_path = file_path
        elif not file_path:
            print("No file selected")

    def handle_find_button(self):
        # Get search term
        search_term = self.find_text.text()

        # Check if file path and search term are set
        if self._selected_file_path and search_term:
            # Create a SearchTermHandler instance
            self.search_term_handler = LanguageHandler(search_term)
            self.main_window._selected_file_path = self._selected_file_path
            self.main_window.create_file_handler()
        elif not self._selected_file_path and not search_term:
            print("No file selected or search term provided")
        elif not search_term:
            print("No search term provided")
        elif not self._selected_file_path:
            print("No file selected")

    def prev_button(self):
        print("Previous button clicked")
        pass

    def start_stop_button(self):
        print("Start/Stop button clicked")
        return True

    def next_button(self):
        print("Next button clicked")
        pass

