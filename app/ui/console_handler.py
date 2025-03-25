# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
"""Console handler module for redirecting stdout to the UI."""

import logging
from PyQt6 import QtWidgets


class ConsoleHandler:
    """Console handler class that redirects stdout to a QTextEdit widget."""

    def __init__(self, text_edit):
        self.output_field = text_edit

    def write(self, text):
        """
        Write text to the output field and log it.

        Parameters:
            text: Text to write to the console
        """
        logging.info(text)
        self.output_field.insertPlainText(text)
        self.output_field.ensureCursorVisible()
        QtWidgets.QApplication.processEvents()  # Ensure the UI updates in real-time
