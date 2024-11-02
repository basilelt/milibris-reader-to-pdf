# cli.py
# Modified on 2024-10-19
# Added functionality to open a browser for user login, process protected content, denoise extracted images, and improve page navigation.

import sys
import os
import argparse
import time
import shutil
import img2pdf
import urllib.request
import cv2
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def denoise_image(file_path: str) -> None:
    """
    Apply denoising to the specified image using OpenCV.
    """
    image = cv2.imread(file_path)
    if image is None:
        print(f"Warning: Unable to read image '{file_path}'. Skipping denoise.", file=sys.stderr)
        return
    denoised = cv2.fastNlMeansDenoisingColored(image, None, h=10, hColor=10, templateWindowSize=7, searchWindowSize=21)
    cv2.imwrite(file_path, denoised)
    print(f"Denoised image saved: {file_path}")

def get_page(image_url: str, subdir: str, page: int) -> None:
    """
    Download a single page image from the URL, denoise it if driver is provided, and save it locally.
    """
    file_name = os.path.join(subdir, f"page-{page:03}.jpg")
    if os.path.isfile(file_name):
        print(f"Image already exists: {file_name}. Skipping download.")
        return
    try:
        if not image_url.startswith('http'):
            image_url = 'https:' + image_url
        print(f"Fetching image from URL: {image_url}")
        with urllib.request.urlopen(image_url) as response, open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        print(f"Downloaded image: {file_name}")
        denoise_image(file_name)
    except Exception as e:
        print(f"Failed to download or denoise image from '{image_url}': {e}", file=sys.stderr)

def generate_pdf(html_input, output_dir: str, save_html: bool = False, pdf_name: str = "output") -> None:
    """
    Extract images from HTML and compile them into a PDF.
    If save_html is True, save the fetched HTML content to the output directory.
    """
    output_subdir = os.path.join(output_dir, pdf_name)
    os.makedirs(output_subdir, exist_ok=True)

    if save_html:
        html_file_path = os.path.join(output_subdir, f"{pdf_name}.html")
        try:
            with open(html_file_path, 'w', encoding='utf-8') as html_file:
                html_file.write(html_input)
            print(f"Saved HTML to '{html_file_path}'")
        except Exception as e:
            print(f"Failed to save HTML to '{html_file_path}': {e}", file=sys.stderr)

    soup = BeautifulSoup(html_input, 'html.parser')
    page = 1
    image_urls = set()
    for div in soup.find_all('div', class_='page'):
        style = div.get('style', '')
        if 'background-image' in style:
            start = style.find('url(') + 4
            end = style.find(')', start)
            if start != -1 and end != -1:
                img_url = style[start:end].strip('\'"')
                image_urls.add(img_url)

    if not image_urls:
        print("No images found in HTML content.", file=sys.stderr)
        return

    for img_url in sorted(image_urls):
        print(f"Extracted image URL: {img_url}")
        get_page(img_url, output_subdir, page)
        page += 1

    image_files = sorted([
        os.path.join(output_subdir, i)
        for i in os.listdir(output_subdir)
        if i.lower().endswith(('.jpg', '.jpeg', '.png'))
    ])

    if not image_files:
        print(f"No images found in '{output_subdir}' to convert to PDF.", file=sys.stderr)
        return

    pdf_path = os.path.join(output_dir, f"{pdf_name}.pdf")
    try:
        with open(pdf_path, "wb") as f:
            f.write(img2pdf.convert(image_files))
        print(f"PDF created at '{pdf_path}'.")
    except Exception as e:
        print(f"Failed to create PDF '{pdf_path}': {e}", file=sys.stderr)

def download_all_pages(driver: webdriver.Chrome) -> None:
    """
    Use Selenium to download the HTML content from the given URL.
    Navigate through all pages by clicking the "Next" button.
    Implements explicit waits to ensure dynamic content loads.
    """
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'currentPage'))
        )
        total_pages = int(driver.find_element(By.CLASS_NAME, 'num-last').text)
        print(f"Total pages: {total_pages}")

        for page_num in range(1, total_pages + 1):
            script = f"Milibris.MultiViewer.reader.controller.goToPage({page_num});"
            driver.execute_script(script)
            time.sleep(1)
            print(f"Navigated to page {page_num}")
    except Exception as e:
        print(f"Error scrolling through pages: {e}", file=sys.stderr)

def download_html(url: str, driver: webdriver.Chrome) -> str:
    """
    Use Selenium to download the HTML content from the given URL.
    Navigate through all pages by clicking the "Next" button.
    Implements explicit waits to ensure dynamic content loads.
    """
    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'currentPage'))
        )
        print(f"Successfully loaded URL: {url}")

        download_all_pages(driver)
        time.sleep(5)  # Wait for all pages to load

        return driver.page_source
    except Exception as e:
        print(f"Error downloading HTML from {url}: {e}", file=sys.stderr)
        return ""

def parse_book_links(html_content: str) -> list:
    """
    Parse the input HTML content to extract book links.
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        book_links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if 'feuilletage.php?issue=' in href:
                full_url = urllib.request.urljoin('https://www.lepointveterinaire.fr/', href)
                book_links.append(full_url)
        print(f"Found {len(book_links)} book links.")
        return book_links
    except Exception as e:
        print(f"Error parsing book links: {e}", file=sys.stderr)
        return []

def main():
    """Main function for the bulk PDF converter with login and denoise images."""
    parser = argparse.ArgumentParser(description='Bulk convert HTML books to PDF.')
    parser.add_argument('output_folder', help='Path to the output folder to save PDFs.')
    parser.add_argument('--save-html', action='store_true', help='Save the fetched HTML content to the output directory.')
    args = parser.parse_args()

    # Set the fixed URL
    input_url = 'https://www.lepointveterinaire.fr/publications/le-point-veterinaire/lire-l-edition-numerique.html'
    output_folder = args.output_folder
    save_html = args.save_html

    if not os.path.isdir(output_folder):
        os.makedirs(output_folder, exist_ok=True)
        print(f"Created output directory: '{output_folder}'")

    # Set up Selenium WebDriver
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Uncomment the following line to run Chrome in headless mode
    # options.add_argument("--headless")
    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"Error initializing Chrome WebDriver: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        # Open the website's login page
        print("Opening login page...")
        driver.get('https://www.lepointveterinaire.fr/espace-membre/s-identifier.html?redirect=/login')
        print("Please log in to the website in the opened browser window.")
        input("After logging in, press Enter here to continue...")

        # Download HTML from the fixed URL
        html_content = download_html(input_url, driver)

        if not html_content:
            print(f"Failed to retrieve HTML content from '{input_url}'.", file=sys.stderr)
            sys.exit(1)

        # Parse book links from the fetched HTML content
        book_links = parse_book_links(html_content)

        if not book_links:
            print("No book links found in the fetched HTML content.", file=sys.stderr)
            sys.exit(1)

        for index, link in enumerate(book_links, start=1):
            try:
                time.sleep(10)  # Wait 10 seconds before processing each book
                print(f"Processing ({index}/{len(book_links)}): {link}")
                # Download the main HTML content for the book
                book_html = download_html(link, driver)

                if not book_html:
                    print(f"Skipped conversion for '{link}' due to empty HTML content.", file=sys.stderr)
                    continue

                # Create a unique name for each PDF based on the link
                pdf_name = f"book_{index}"

                # Process the HTML content to generate PDF
                generate_pdf(
                    html_input=book_html, 
                    output_dir=output_folder, 
                    save_html=save_html, 
                    pdf_name=pdf_name
                )
                print(f"Converted '{link}' to PDF.\n")
            except Exception as e:
                print(f"Failed to convert '{link}': {e}", file=sys.stderr)
        print("All books have been processed.")
    finally:
        driver.quit()
        print("Selenium WebDriver closed.")

if __name__ == "__main__":
    main()
