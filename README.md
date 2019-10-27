# milibris-reader-to-pdf

[milibris](https://www.milibris.com/) publications usually can not be downloaded as PDF file.

This script:
- extracts jpeg image urls (one for each page) from html source code
- downloads each page as a jpeg file
- assembles the pages into a unique pdf file using [img2pdf](https://gitlab.mister-muffin.de/josch/img2pdf)

## Usage
 - open the publication with the web reader
 - browse each page, one after the other, by clickling 'next' button (not convenient, but otherwise the correct html is not generated)
 - save the web page as `.html` file
 - run this python script on the `.html` file

