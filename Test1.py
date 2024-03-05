import pypdf 

# Проверка локальных путей
# import os
# current_working_directory = os.getcwd()
# print('Path:', current_working_directory)

pdf_path = 'IN/Test.pdf'

with open(pdf_path, 'rb') as pdf_file:
    pdf_reader = pypdf.PdfReader(pdf_file) 
    meta = pdf_reader.metadata
    print('=======================')
    print(f'Number of Pages in PDF File is {len(pdf_reader.pages)}') 
    print('Author: ', meta.author)
    print('Creator: ', meta.creator)
    print('Producer: ', meta.producer)
    print('Subject: ', meta.subject)
    print('Title: ', meta.title)

    print('CreationDate: ', meta.creation_date)
    print('ModDate: ', meta.modification_date)

    print('=======================')
