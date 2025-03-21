# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
"""UI element handling functionality for the application."""

from PyQt6 import QtWidgets
from app.processing.language_handler import LanguageHandler


class ElementHandler:
    """Handles UI elements and their interactions in the application."""

    def __init__(self, main_window):
        # Get reference to the main window
        self.main_window = main_window
        self.selected_file_path = None
        self.search_term_handler = None

        # Find all UI elements
        self.select_file_button = self.main_window.findChild(
            QtWidgets.QPushButton, "select_file_button"
        )
        self.select_file_text = self.main_window.findChild(
            QtWidgets.QLineEdit, "select_file_text"
        )
        self.find_text = self.main_window.findChild(QtWidgets.QLineEdit, "find_text")
        self.find_button = self.main_window.findChild(
            QtWidgets.QPushButton, "find_button"
        )

        self.preview_element = self.main_window.findChild(
            QtWidgets.QGraphicsView, "preview_frame"
        )

        self.prev_button = self.main_window.findChild(
            QtWidgets.QPushButton, "prev_button"
        )
        self.start_stop_button = self.main_window.findChild(
            QtWidgets.QPushButton, "start_stop_button"
        )
        self.next_button = self.main_window.findChild(
            QtWidgets.QPushButton, "next_button"
        )

        self.progress_bar = self.main_window.findChild(
            QtWidgets.QProgressBar, "progress_bar"
        )
        self.information_output = self.main_window.findChild(
            QtWidgets.QTextEdit, "information_output"
        )

        # Connect button click events to methods
        self.connect_buttons()

    def connect_buttons(self):
        """Connect UI buttons to their handler methods."""
        # Connect the select file button to the file selector
        self.select_file_button.clicked.connect(self.show_file_selector)

        # Connect the find button to the find handler
        self.find_button.clicked.connect(self.handle_find_button)

        # Connect the previous button to the previous handler
        self.prev_button.clicked.connect(self.handle_prev_button)

        # Connect the start/stop button to the start/stop handler
        self.start_stop_button.clicked.connect(self.handle_start_stop_button)

        # Connect the next button to the next handler
        self.next_button.clicked.connect(self.handle_next_button)

    def show_file_selector(self):
        """Show file selector dialog and handle selected file."""
        file_dialog = QtWidgets.QFileDialog()
        options = file_dialog.options()
        file_path, _ = file_dialog.getOpenFileName(
            self.main_window,
            "Open File",
            "/",
            "Video Files (*.mp4 *.mkv)",
            options=options,
        )

        # Retrieve search term
        if file_path:
            self.select_file_text.setText(file_path.split("/")[-1])
            # Store file path for later use when find button is clicked
            self.selected_file_path = file_path
        elif not file_path:
            print("No file selected")

    def handle_find_button(self):
        """Handle find button click to start search with selected file and search term."""
        # Get search term
        search_term = self.find_text.text()

        # Check if file path and search term are set
        if self.selected_file_path and search_term:
            # Create a SearchTermHandler instance
            self.search_term_handler = LanguageHandler(search_term)
            # Use property setter or method to safely set main window's file path
            self.main_window.selected_file_path = self.selected_file_path
            self.main_window.create_file_handler()
        elif not self.selected_file_path and not search_term:
            print("No file selected or search term provided")
        elif not search_term:
            print("No search term provided")
        elif not self.selected_file_path:
            print("No file selected")

    def handle_prev_button(self):
        """Handle previous button click to show previous frame."""
        print("Previous button clicked")

    def handle_start_stop_button(self):
        """
        Handle start/stop button click to pause/resume processing.

        Returns:
            bool: Processing state
        """
        print("Start/Stop button clicked")
        return True

    def handle_next_button(self):
        """Handle next button click to show next frame."""
        print("Next button clicked")
