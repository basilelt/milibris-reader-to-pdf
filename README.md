# milibris-reader-to-pdf

**Forked from [milibris-reader-to-pdf](https://gitlab.com/fabrice.aeschbacher/milibris-reader-to-pdf)**

[milibris](https://www.milibris.com/) publications usually cannot be downloaded as PDF files.

This project provides tools to:

- Extract JPEG image URLs (one for each page) from HTML source code
- Download each page as a JPEG file
- Assemble the pages into a single PDF file using [img2pdf](https://gitlab.mister-muffin.de/josch/img2pdf)
- **Additionally**, offers a graphical user interface (GUI) for easier usage on macOS

## Features

- **Command-Line Interface (CLI):** Traditional method for advanced users.
- **Graphical User Interface (GUI):** User-friendly interface for selecting input folders and output destinations.
- **Automated macOS Application:** Convenient `.app` bundle for seamless integration with macOS.

## Getting Started

### Prerequisites

- **Python 3.12** (for CLI usage)
- **macOS** (for using the packaged `.app`)

### Installation

#### Using the Graphical User Interface (GUI) on macOS

1. **Download the macOS Application:**

   - Download the `MilibrisReaderToPDF-macOS.app` artifact.

2. **Move the Application to Applications Folder:**

   ```bash
   mv MilibrisReaderToPDF-macOS.app /Applications/
   ```

### Usage

#### Graphical User Interface (GUI) on macOS

1. **Launch the Application:**
   - Open `MilibrisReaderToPDF-macOS.app` from your Applications folder.

2. **Select Input Folder:**
   - Click "Select Input Folder" or drag and drop the folder containing your `.html` files.

3. **Select Output Destination:**
   - Click "Select Output Destination" or drag and drop your desired save location for the PDF.

4. **Convert to PDF:**
   - Click "Convert to PDF" to initiate the conversion process.
   - A notification will appear upon successful completion.

### Troubleshooting

- **Application Not Launching (GUI):**
  - Verify that the application is in the Applications folder.
  - If you encounter security warnings, go to `System Preferences` > `Security & Privacy` and allow the application to run.

- **Conversion Errors:**
  - Ensure that the `.html` files are correctly generated and not corrupted.
  - Check the console or application logs for detailed error messages.

## Building the macOS Application

For developers interested in building the macOS application from source:

1. **Ensure All Dependencies Are Installed:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Build the Application:**

   ```bash
   python setup.py py2app
   ```

3. **Locate the Built Application:**
   - The `.app` bundle will be located in the `dist/` directory.

## Continuous Integration

This project uses **GitHub Actions** to automate the build process for the macOS application. On every push to the `main` branch:

1. **Builds the Application:**
   - Compiles the Python scripts into a standalone `.app` bundle using `py2app`.

2. **Uploads the Artifact:**
   - Makes the built `.app` available as a downloadable artifact.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Original code by Fabrice Aeschbacher is used under the MIT License.

Icon from [https://www.flaticon.com/free-icons/books](https://www.flaticon.com/free-icons/books) created by [popo2021](https://www.flaticon.com/authors/popo2021) is used under the CC 3.0 BY license.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## Acknowledgements

- [Fabrice Aeschbacher](https://gitlab.com/fabrice.aeschbacher/milibris-reader-to-pdf) for the original script.
- [img2pdf](https://gitlab.mister-muffin.de/josch/img2pdf) for PDF conversion.
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/intro) for the GUI framework.
- [GitHub Actions](https://github.com/features/actions) for continuous integration.

---