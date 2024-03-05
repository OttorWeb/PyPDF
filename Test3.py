import pypdf

reader = pypdf.PdfReader('IN/Test.pdf')
print('=======================')
page = reader.pages[0]
print(page.extract_text())
print('=======================')
page = reader.pages[1]
print(page.extract_text())
print('=======================')
page = reader.pages[2]
print(page.extract_text())
print('=======================||||||||||')

print(page.extract_text(0, 10))
