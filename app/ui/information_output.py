# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Methods to output console logs to the UI
from PyQt6 import QtWidgets


class TextStream:
    def __init__(self, text_edit):
        self.output_field = text_edit
        self.line_count = 0

    def write(self, text):
        self.output_field.insertPlainText(text)
        self.output_field.ensureCursorVisible()
        QtWidgets.QApplication.processEvents()  # Ensure the UI updates in real-time
        self.line_count += 1
        if self.line_count >= 100:
            self.output_field.clear()
            self.line_count = 0

    def flush(self):
        pass