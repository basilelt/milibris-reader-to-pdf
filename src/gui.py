# gui.py
# Modified on 2024-10-19 by BasileLT
# - Combined GUI and PDF generation functionalities
#
# Original code by Fabrice Aeschbacher under the MIT License.

import sys
import os
import mmap
import urllib.request
import shutil
import img2pdf
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt

# Constants for parsing HTML content
PATTERN_START = b'background-image: url(&quot;//'
PATTERN_START_SIZE = len(PATTERN_START)
PATTERN_END = b'&quot;'
PATTERN_END_SIZE = len(PATTERN_END)

def get_page(url: str, subdir: str, page: int) -> None:
    """
    Download a single page image from the URL and save it locally.
    """
    file_name = os.path.join(subdir, f"page-{page:03}.jpg")
    if os.path.isfile(file_name):
        return
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

def generate_pdf(html_file: str, output_dir: str) -> None:
    """
    Extract images from HTML and compile them into a PDF.
    """
    basename = os.path.basename(html_file)
    name = os.path.splitext(basename)[0]
    output_subdir = os.path.join(output_dir, name)
    os.makedirs(output_subdir, exist_ok=True)

    with open(html_file, encoding='utf-8') as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        start = mm.find(PATTERN_START, 0)
        page = 1
        while start != -1:
            start += PATTERN_START_SIZE
            end = mm.find(PATTERN_END, start)
            bytes_array = mm[start:end]
            url = 'https://' + bytes_array.decode('utf-8')
            get_page(url, output_subdir, page)
            start = mm.find(PATTERN_START, end)
            page += 1
        mm.close()

    pdf_path = os.path.join(output_dir, f"{name}.pdf")
    image_files = sorted([
        os.path.join(output_subdir, i)
        for i in os.listdir(output_subdir)
        if i.endswith(('.jpg', '.png'))
    ])
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(image_files))

class PDFConverterGUI(QWidget):
    """
    A PyQt6-based GUI for converting HTML files to PDF.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Milibris Reader to PDF Converter")
        self.setGeometry(100, 100, 400, 200)
        self.input_folder = ""
        self.output_folder = ""
        self.setup_ui()

    def setup_ui(self):
        """Set up the graphical user interface."""
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
        """Select the input folder."""
        folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if folder:
            self.input_folder = folder
            self.input_label.setText(f"Input Folder: {folder}")

    def select_output_destination(self):
        """Select the output destination."""
        folder = QFileDialog.getExistingDirectory(self, "Select Output Destination")
        if folder:
            self.output_folder = folder
            self.output_label.setText(f"Output Destination: {folder}")

    def convert_to_pdf(self):
        """Convert selected HTML files to PDF."""
        try:
            if not self.input_folder or not self.output_folder:
                QMessageBox.warning(
                    self, "Missing Information",
                    "Please select both input folder and output destination."
                )
                return

            for file_name in os.listdir(self.input_folder):
                if file_name.lower().endswith('.html'):
                    html_path = os.path.join(self.input_folder, file_name)
                    generate_pdf(html_path, self.output_folder)

            QMessageBox.information(self, "Success", "PDF conversion completed successfully.")
        except FileNotFoundError as e:
            QMessageBox.critical(self, "File Error", f"Required file or directory not found:\n{e}")
        except PermissionError as e:
            QMessageBox.critical(self, "Permission Error", f"Access denied:\n{e}")
        except OSError as e:
            QMessageBox.critical(self, "System Error", f"OS error occurred:\n{e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unexpected error:\n{type(e).__name__}: {e}")

def main():
    """Launch the PDF converter GUI application."""
    try:
        app = QApplication(sys.argv)
        gui = PDFConverterGUI()
        gui.show()
        sys.exit(app.exec())
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
