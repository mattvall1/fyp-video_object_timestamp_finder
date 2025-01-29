# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Main view
import sys
from datetime import datetime
import logging
from PyQt6 import QtWidgets, uic, QtMultimediaWidgets
from app.processing.file_handler import FileHandler
from app.ui.console_handler import ConsoleHandler

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.file_handler = None
        self.select_file_text = None
        uic.loadUi('ui/main_view.ui', self)
        self.show()

        # Configure
        logging.basicConfig(filename=f'logs/{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}_log.txt', level=logging.INFO)

        # Access elements from UI
        self.select_file_button = self.findChild(QtWidgets.QPushButton, 'select_file_button')
        self.find_button = self.findChild(QtWidgets.QPushButton, 'find_button')
        self.preview_element = self.findChild(QtWidgets.QGraphicsView, 'preview_frame')
        self.information_output = self.findChild(QtWidgets.QTextEdit, 'information_output')
        self.progress_bar = self.findChild(QtWidgets.QProgressBar, 'progress_bar')

        # Redirect standard output to console
        sys.stdout = ConsoleHandler(self.information_output)

        # Connect button click event to method
        self.select_file_button.clicked.connect(self.show_file_selector)

    def show_file_selector(self):
        file_dialog = QtWidgets.QFileDialog()
        options = file_dialog.options()
        file_path, _ = file_dialog.getOpenFileName(self, "Open File", "/", "Video Files (*.mp4 *.mkv)", options=options)

        if file_path:
            self.select_file_text.setText(file_path.split('/')[-1])
            self.find_button.clicked.connect(lambda: self.create_file_handler(file_path))

    def create_file_handler(self, file_path):
        # Create file handler instance and play video
        self.file_handler = FileHandler(file_path, preview_element=self.preview_element, progress_bar=self.progress_bar)
        self.file_handler.split_video()



app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec())