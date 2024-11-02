# Modified on 2024-10-19 by BasileLT
# - Added GUI
#
# Original code by Fabrice Aeschbacher under the MIT License.

import sys
import os
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt

class PDFConverterGUI(QWidget):
    """
    A PyQt6-based GUI for converting Milibris Reader HTML files to PDF format.

    This class provides a graphical interface allowing users to:
    - Select an input folder containing HTML files
    - Choose an output destination for PDF files
    - Convert HTML files to PDF using gen_pdf.py

    Attributes:
        input_folder (str): Path to selected input directory
        output_folder (str): Path to selected output directory
        input_label (QLabel): Display for input folder path
        output_label (QLabel): Display for output folder path
        input_button (QPushButton): Button to select input folder
        output_button (QPushButton): Button to select output folder
        convert_button (QPushButton): Button to initiate conversion

    Inherits:
        QWidget: Base class from PyQt6 for GUI widgets
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Milibris Reader to PDF Converter")
        self.setGeometry(100, 100, 400, 200)
        self.input_folder = ""
        self.output_folder = ""
        self.setup_ui()

    def setup_ui(self):
        """Set up the graphical user interface for the PDF converter application.
        
        Creates and arranges the following UI elements:
        - Input folder selection button and label
        - Output destination button and label 
        - Convert button to trigger PDF conversion
        - Vertical layout to organize all elements
        """
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
        """Open a file dialog to select the input folder for PDF conversion.
        
        Opens a QFileDialog for folder selection and updates the GUI state:
        - Stores selected path in self.input_folder
        - Updates input_label text to show selected path
        """
        folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if folder:
            self.input_folder = folder
            self.input_label.setText(f"Input Folder: {folder}")

    def select_output_destination(self):
        """Open a file dialog to select the output destination for converted PDFs.
        
        Opens a QFileDialog for folder selection and updates the GUI state:
        - Stores selected path in self.output_folder
        - Updates output_label text to show selected destination
        """
        folder = QFileDialog.getExistingDirectory(self, "Select Output Destination")
        if folder:
            self.output_folder = folder
            self.output_label.setText(f"Output Destination: {folder}")

    def convert_to_pdf(self):
        """Convert HTML files in the input folder to PDF format.
        
        Processes all HTML files in the selected input folder using gen_pdf.py script.
        Shows appropriate message dialogs for success/failure states.
        
        Error handling:
        - Validates input/output folder selection
        - Catches subprocess execution errors
        - Handles unexpected exceptions
        
        Requirements:
        - Input folder must contain HTML files
        - gen_pdf.py must exist in the same directory
        - Both input_folder and output_folder must be selected
        """
        try:
            if not self.input_folder or not self.output_folder:
                QMessageBox.warning(self, "Missing Information", "Please select both input folder and output destination.")
                return

            # Assuming gen-pdf.py is in the src/ directory
            gen_pdf_path = os.path.join(os.path.dirname(__file__), 'gen_pdf.py')

            # Iterate through HTML files in the input folder
            for file_name in os.listdir(self.input_folder):
                if file_name.lower().endswith('.html'):
                    html_path = os.path.join(self.input_folder, file_name)
                    subprocess.run(['python3', gen_pdf_path, html_path, self.output_folder], check=True)

            QMessageBox.information(self, "Success", "PDF conversion completed successfully.")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Conversion Error",
                                 f"An error occurred during conversion:\n{e}")
        except FileNotFoundError as e:
            QMessageBox.critical(self, "File Error",
                                 f"Required file or directory not found:\n{e}")
        except PermissionError as e:
            QMessageBox.critical(self, "Permission Error",
                                 f"Access denied. Please check folder permissions:\n{e}")
        except OSError as e:
            QMessageBox.critical(self, "System Error",
                                 f"Operating system error occurred:\n{e}")
        except Exception as e:
            QMessageBox.critical(self, "Error",
                                 f"An unexpected error occurred:\n{type(e).__name__}: {e}")

def main():
    """Launch the PDF converter GUI application.
    
    Creates QApplication instance and shows main window.
    Handles application exit and cleanup.
    """
    try:
        app = QApplication(sys.argv)
        gui = PDFConverterGUI()
        gui.show()
        return sys.exit(app.exec())
    except RuntimeError as e:
        print(f"Qt runtime error: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"System error: {e}", file=sys.stderr) 
        return 1
    except KeyboardInterrupt:
        print("\nApplication terminated by user")
        return 0

if __name__ == "__main__":
    main()
