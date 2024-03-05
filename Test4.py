from pypdf import PdfReader
import PIL
import os

# Системные пути к файлам
# import sys
from pprint import pprint
# print("==============================================================")
# pprint(sys.path)
# print("==============================================================")

user_file = "IN/Test_Img.pdf"
reader = PdfReader(user_file)

page = reader.pages[0]
count = 0

pprint(page.images)


for image_file_object in page.images:
    # Если запись в коренвой коталог скрипта:
    # fs = str(count) + '-' + image_file_object.name
    # Если запись в указанный коталог скрипта:
    fs = os.path.join('OUT/IMG/', str(count) + '-' + image_file_object.name)
    with open(fs, "wb") as fp:
        fp.write(image_file_object.data)
        count += 1
