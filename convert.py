import pdftotext
import os
from pathlib import Path
from pytesseract import image_to_pdf_or_hocr, image_to_string

input_path = Path("input")
temp_path = Path("temp")

def convert_systeme_u(src, temp):
    if not temp.exists():
        temp.mkdir(parents=True)
    for item in os.listdir(src):
        if item.endswith('.pdf'):
            with open(src/item,"rb") as pdf_file:
                pdf = pdftotext.PDF(pdf_file)
                if (len(pdf) == 1):
                    with open(temp/item.replace('pdf','u.txt'), "w+") as txt:
                        txt.write(pdf[0])

def convert_lidl(src,temp,extension='jpg'):
    if not temp.exists():
        temp.mkdir(parents=True)
    for item in os.listdir(src):
        if item.endswith(f'.{extension}'):
            string_content = image_to_string(str(src/item))
            # print(string_content)
            # content = image_to_pdf_or_hocr(str(target/item))
            # if (len(pdf) == 1):
            with open(temp/(item.replace(extension,'lidl.txt')), "w+") as txt:
                txt.write(string_content)
            # print(content)
            # with open(target/item.replace('.jpg','lidl.pdf'), 'wb+') as f:
            #     f.write(content)CACAT
            # with open(target/item.replace('.jpg','lidl.pdf'), 'rb') as f:
            #     pdf = pdftotext.PDF(f)
            #     print(pdf[0])
            # break

if __name__ == "__main__":
    convert_systeme_u(input_path/"u", temp_path/"u")
    convert_lidl(input_path/"lidl", temp_path/"lidl")
    convert_lidl(input_path/"lidl", temp_path/"lidl", 'png')