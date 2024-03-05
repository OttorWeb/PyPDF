import pypdf
# Находим путь к PDF
pdf_path = 'd:/WORK/Python/PDF/APP/Test.pdf'

# создаём объект файла PDF
pdfFileObj = open(pdf_path, 'rb')

# создаём объект считывателя PDF
pdfReaded = pypdf.PdfReader(pdfFileObj)

# Создаём словарь для извлечения текста из каждого изображения
text_per_page = {}
# Извлекаем страницы из PDF
for pagenum, page in enumerate(pdfReaded):
    
    # Инициализируем переменные, необходимые для извлечения текста со страницы
    pageObj = pdfReaded.pages[pagenum]
    page_text = []
    line_format = []
    text_from_images = []
    text_from_tables = []
    page_content = []
    # Инициализируем количество исследованных таблиц
    table_num = 0
    first_element= True
    table_extraction_flag= False
    # Открываем файл pdf
    pdf = pdfplumber.open(pdf_path)
    # Находим исследуемую страницу
    page_tables = pdf.pages[pagenum]
    # Находим количество таблиц на странице
    tables = page_tables.find_tables()


    # Находим все элементы
    page_elements = [(element.y1, element) for element in page._objs]
    # Сортируем все элементы по порядку нахождения на странице
    page_elements.sort(key=lambda a: a[0], reverse=True)

    # Находим элементы, составляющие страницу
    for i,component in enumerate(page_elements):
        # Извлекаем положение верхнего края элемента в PDF
        pos= component[0]
        # Извлекаем элемент структуры страницы
        element = component[1]
        
        # Проверяем, является ли элемент текстовым
        if isinstance(element, LTTextContainer):
            # Проверяем, находится ли текст в таблице
            if table_extraction_flag == False:
                # Используем функцию извлечения текста и формата для каждого текстового элемента
                (line_text, format_per_line) = text_extraction(element)
                # Добавляем текст каждой строки к тексту страницы
                page_text.append(line_text)
                # Добавляем формат каждой строки, содержащей текст
                line_format.append(format_per_line)
                page_content.append(line_text)
            else:
                # Пропускаем текст, находящийся в таблице
                pass

        # Проверяем элементы на наличие изображений
        if isinstance(element, LTFigure):
            # Вырезаем изображение из PDF
            crop_image(element, pageObj)
            # Преобразуем обрезанный pdf в изображение
            convert_to_images('cropped_image.pdf')
            # Извлекаем текст из изображения
            image_text = image_to_text('PDF_image.png')
            text_from_images.append(image_text)
            page_content.append(image_text)
            # Добавляем условное обозначение в списки текста и формата
            page_text.append('image')
            line_format.append('image')

        # Проверяем элементы на наличие таблиц
        if isinstance(element, LTRect):
            # Если первый прямоугольный элемент
            if first_element == True and (table_num+1) <= len(tables):
                # Находим ограничивающий прямоугольник таблицы
                lower_side = page.bbox[3] - tables[table_num].bbox[3]
                upper_side = element.y1 
                # Извлекаем информацию из таблицы
                table = extract_table(pdf_path, pagenum, table_num)
                # Преобразуем информацию таблицы в формат структурированной строки
                table_string = table_converter(table)
                # Добавляем строку таблицы в список
                text_from_tables.append(table_string)
                page_content.append(table_string)
                # Устанавливаем флаг True, чтобы избежать повторения содержимого
                table_extraction_flag = True
                # Преобразуем в другой элемент
                first_element = False
                # Добавляем условное обозначение в списки текста и формата
                page_text.append('table')
                line_format.append('table')

            # Проверяем, извлекли ли мы уже таблицы из этой страницы
            if element.y0 >= lower_side and element.y1 <= upper_side:
                pass
            elif not isinstance(page_elements[i+1][1], LTRect):
                table_extraction_flag = False
                first_element = True
                table_num+=1


    # Создаём ключ для словаря
    dctkey = 'Page_'+str(pagenum)
    # Добавляем список списков как значение ключа страницы
    text_per_page[dctkey]= [page_text, line_format, text_from_images,text_from_tables, page_content]

# Закрываем объект файла pdf
pdfFileObj.close()

# Удаляем созданные дополнительные файлы
os.remove('cropped_image.pdf')
os.remove('PDF_image.png')

# Удаляем содержимое страницы
result = ''.join(text_per_page['Page_0'][4])
print(result)