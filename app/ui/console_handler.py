# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Methods to output console logs to the UI
from PyQt6 import QtWidgets
import logging


class ConsoleHandler:
    def __init__(self, text_edit):
        self.output_field = text_edit
        self.line_count = 0
        pass

    def write(self, text):
        logging.info(text)
        self.output_field.insertPlainText(text)
        self.output_field.ensureCursorVisible()
        QtWidgets.QApplication.processEvents()  # Ensure the UI updates in real-time

    def flush(self):
        pass