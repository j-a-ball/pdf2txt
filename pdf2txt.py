__author__ = "Jon Ball"
__version__ = "Fall 2023"

# Dependencies: tesseract poppler
# Python 3.9
# !pip install pdf2image PIL pytesseract

from pdf2image import convert_from_path
#pdf2image req'd PIL due to error
from PIL import Image
import pytesseract
import os

class pdf2txt():
    def __init__(self, pdf_dir, txt_dir):
        self.pdf_dir = pdf_dir
        self.txt_dir = txt_dir
        # Create the output directory if it doesn't exist
        if not os.path.exists(self.txt_dir):
            os.makedirs(self.txt_dir)

    def convert(self, pdf_file):
        doc = convert_from_path(os.path.join(self.pdf_dir, pdf_file))
        txt_list = []
        for page_data in doc:
            txt_list.append(pytesseract.image_to_string(page_data))
        txt = "<sep>".join(txt_list)
        with open(os.path.join(self.txt_dir, f"{pdf_file[:-4]}.txt"), "w") as outfile:
            outfile.write(txt)
        return txt
