import pdftotext
import os
from pathlib import Path
target_path = Path("data")
def convert(target):
    
    for item in os.listdir(target):
        if item.endswith('.pdf'):
            with open(target/item,"rb") as pdf_file:
                pdf = pdftotext.PDF(pdf_file)
                if (len(pdf) == 1):
                    with open(target/item.replace('pdf','txt'), "w+") as txt:
                        txt.write(pdf[0])

if __name__ == "__main__":
    convert(target_path)