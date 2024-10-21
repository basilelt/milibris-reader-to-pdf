# Modified on 2024-10-19 by BasileLT
# - Added GUI
#
# Original code by Fabrice Aeschbacher under the MIT License.

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt
import subprocess

class PDFConverterGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Milibris Reader to PDF Converter")
        self.setGeometry(100, 100, 400, 200)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Input Folder Selection
        self.input_label = QLabel("No input folder selected.")
        self.input_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_button = QPushButton("Select Input Folder")
        self.input_button.clicked.connect(self.select_input_folder)

        # Output Destination Selection
        self.output_label = QLabel("No output destination selected.")
        self.output_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.output_button = QPushButton("Select Output Destination")
        self.output_button.clicked.connect(self.select_output_destination)

        # Convert Button
        self.convert_button = QPushButton("Convert to PDF")
        self.convert_button.clicked.connect(self.convert_to_pdf)

        # Add widgets to layout
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_button)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_button)
        layout.addWidget(self.convert_button)

        self.setLayout(layout)

    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if folder:
            self.input_folder = folder
            self.input_label.setText(f"Input Folder: {folder}")

    def select_output_destination(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Destination")
        if folder:
            self.output_folder = folder
            self.output_label.setText(f"Output Destination: {folder}")

    def convert_to_pdf(self):
        try:
            if not hasattr(self, 'input_folder') or not hasattr(self, 'output_folder'):
                QMessageBox.warning(self, "Missing Information", "Please select both input folder and output destination.")
                return

            # Assuming gen-pdf.py is in the src/ directory
            gen_pdf_path = os.path.join(os.path.dirname(__file__), 'gen-pdf.py')

            # Iterate through HTML files in the input folder
            for file_name in os.listdir(self.input_folder):
                if file_name.lower().endswith('.html'):
                    html_path = os.path.join(self.input_folder, file_name)
                    subprocess.run(['python3', gen_pdf_path, html_path], check=True)

            QMessageBox.information(self, "Success", "PDF conversion completed successfully.")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Conversion Error", f"An error occurred during conversion:\n{e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred:\n{e}")

def main():
    app = QApplication(sys.argv)
    gui = PDFConverterGUI()
    gui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()