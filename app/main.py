# © 2024 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Main application entry point
import sys
from PyQt6 import QtWidgets
from global_tools import Tools
from app.ui.main_view import MainWindow

def main():
    # Create all required directories
    Tools.create_directories()
    Tools.clear_frame_directories()

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()