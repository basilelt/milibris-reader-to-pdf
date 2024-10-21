#!/usr/bin/python3
#
# Copyright 2019 Fabrice Aeschbacher <fabrice.aeschbacher@gmail.com>
#
# Usage:
# - open book with the web reader
# - open each page, one after the other, by clickling 'next'
# - save as .html
# - run this python script on the .html file

import os
import sys
import mmap
import urllib.request
import shutil
import img2pdf  # python3-img2pdf
    

pattern_start = b'background-image: url(&quot;//'
pattern_start_sz = len(pattern_start)
pattern_end   = b'&quot;'
pattern_end_sz = len(pattern_end)

def getpage(url, subdir, page):
    print(url)
    print(page)
    file_name = os.path.join(subdir, f"page-{page:03}")
    if os.path.isfile(file_name):
        # no need to download again if already there
        return
    # Download the file from `url` and save it locally under `file_name`:
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

def main():
    if len(sys.argv) < 2:
        sys.exit(1)
    
    html_file = sys.argv[1]
    basename = os.path.basename(html_file)
    # split e.g. 'name.html' into 'name' and '.html'
    (name, ext) = os.path.splitext(basename)
    try:
        os.mkdir(name)
    except FileExistsError:
        pass

    with open(html_file) as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        start = mm.find(pattern_start, 0)
        page = 1
        while start != -1:
            start = start + pattern_start_sz
            end = mm.find(pattern_end, start)
            bytes_array = mm[start:end]
            url = 'https://' + str(bytes_array, 'utf-8')
            getpage(url, name, page)
            start = mm.find(pattern_start, end)
            page = page +1
        mm.close()

    with open(f"{name}.pdf", "wb") as f:
        f.write(img2pdf.convert(sorted([os.path.join(name, i) for i in os.listdir(name)])))

if __name__ == "__main__":
    main()
