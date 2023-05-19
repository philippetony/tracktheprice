import pdftotext
import os
from pathlib import Path
from pytesseract import image_to_pdf_or_hocr, image_to_string

target_path = Path("data")
def convert_systeme_u(target):
    for item in os.listdir(target):
        if item.endswith('.pdf'):
            with open(target/item,"rb") as pdf_file:
                pdf = pdftotext.PDF(pdf_file)
                if (len(pdf) == 1):
                    with open(target/item.replace('pdf','u.txt'), "w+") as txt:
                        txt.write(pdf[0])

def convert_lidl(target):
    for item in os.listdir(target):
        if item.endswith('.jpg'):
            string_content = image_to_string(str(target/item))
            print(string_content)
            content = image_to_pdf_or_hocr(str(target/item))
            # if (len(pdf) == 1):
            #     with open(target/item.replace('pdf','lidl.txt'), "w+") as txt:
            #         txt.write(pdf[0])
            # print(content)
            with open(target/item.replace('.jpg','lidl.pdf'), 'wb+') as f:
                f.write(content)
            with open(target/item.replace('.jpg','lidl.pdf'), 'rb') as f:
                pdf = pdftotext.PDF(f)
                print(pdf[0])
            break

if __name__ == "__main__":
    # convert_systeme_u(target_path)
    convert_lidl(target_path)