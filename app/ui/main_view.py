# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Main view
import sys
from PyQt6 import QtWidgets, uic

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.select_file_text = None
        uic.loadUi('ui/main_view.ui', self)
        self.show()

        # Access button and line edit widgets
        self.select_file_button = self.findChild(QtWidgets.QPushButton, 'select_file_button')

        # Connect button click event to method
        self.select_file_button.clicked.connect(self.show_file_selector)

    # Open file selector dialog
    def show_file_selector(self):
        file_dialog = QtWidgets.QFileDialog()
        options = file_dialog.options()
        file_path = file_dialog.getOpenFileName(self, "Open File", "", "All Files (*)", options=options)

        # Display the file name (no path) in the widget
        if file_path:
            self.select_file_text.setText(file_path[0].split('/')[-1])




app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec())