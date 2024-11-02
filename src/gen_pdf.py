"""
gen_pdf.py - PDF Generator from Milibris Reader HTML Files

This module extracts image URLs from Milibris Reader HTML files, downloads the images,
and combines them into a single PDF document. It processes HTML files saved from
the Milibris web reader interface.

Usage:
    python3 gen_pdf.py <html_file>

Dependencies:
    - img2pdf: For PDF generation
    - mmap: For efficient HTML file processing
    - urllib: For downloading page images

Original work by Fabrice Aeschbacher
Modified by BasileLT
License: MIT
"""

#!/usr/bin/python3
#
# Copyright 2019 Fabrice Aeschbacher <fabrice.aeschbacher@gmail.com>
#
# Usage:
# - open book with the web reader
# - open each page, one after the other, by clicking 'next'
# - save as .html
# - run this python script on the .html file

import os
import sys
import mmap
import urllib.request
import shutil
import img2pdf  # python3-img2pdf

# Constants for parsing HTML content
PATTERN_START = b'background-image: url(&quot;//'
PATTERN_START_SIZE = len(PATTERN_START)
PATTERN_END = b'&quot;'
PATTERN_END_SIZE = len(PATTERN_END)

def get_page(url: str, subdir: str, page: int) -> None:
    """
    Download a single page from the Milibris reader and save it as an image file.

    Args:
        url (str): The URL of the page image to download
        subdir (str): The subdirectory where the image will be saved
        page (int): The page number (used for filename generation)

    Returns:
        None

    Note:
        If the file already exists, the download is skipped to avoid redundant operations.
        Files are saved with format 'page-XXX' where XXX is the zero-padded page number.
    """
    print(url)
    print(page)
    file_name = os.path.join(subdir, f"page-{page:03}")
    if os.path.isfile(file_name):
        # no need to download again if already there
        return
    # Download the file from `url` and save it locally under `file_name`:
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

def main() -> None:
    """
    Process an HTML file from Milibris Reader to extract and combine pages into a PDF.

    Command-line Usage:
        python gen_pdf.py <html_file>

    Args:
        Expected from sys.argv[1]: Path to HTML file from Milibris Reader

    Returns:
        None

    Exit Codes:
        1: If no HTML file is provided as argument
        0: On successful execution

    The function:
    1. Creates a directory named after the HTML file
    2. Extracts image URLs from the HTML using memory mapping
    3. Downloads each page as an image
    4. Combines all images into a single PDF file
    """
    if len(sys.argv) < 2:
        sys.exit(1)

    html_file = sys.argv[1]
    basename = os.path.basename(html_file)
    # split e.g. 'name.html' into 'name' and '.html'
    name = os.path.splitext(basename)[0]
    try:
        os.mkdir(name)
    except FileExistsError:
        pass

    # Add explicit UTF-8 encoding when opening HTML file
    with open(html_file, encoding='utf-8') as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        start = mm.find(PATTERN_START, 0)
        page = 1
        while start != -1:
            start = start + PATTERN_START_SIZE
            end = mm.find(PATTERN_END, start)
            bytes_array = mm[start:end]
            url = 'https://' + str(bytes_array, 'utf-8')
            get_page(url, name, page)
            start = mm.find(PATTERN_START, end)
            page = page + 1
        mm.close()

    with open(f"{name}.pdf", "wb") as f:
        f.write(img2pdf.convert(sorted([os.path.join(name, i) for i in os.listdir(name)])))

if __name__ == "__main__":
    main()
