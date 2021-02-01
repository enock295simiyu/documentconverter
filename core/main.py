from PIL import Image
from pdf2image import convert_from_path
from docx2pdf import convert
import pdfkit
import logging
import traceback
import PyPDF2
import os
import img2pdf
from documentconverter.settings import MEDIA_ROOT
from fpdf import FPDF


class Converter:
    def get_document_name_and_extension(self, upload_url):
        extension_url = upload_url
        name = upload_url.split('/')[-1].split('.')[0]

        extension = extension_url.split('.')[-1]
        return name, extension


class ImageDocuments(Converter):
    def convert_img_to_pdf(self, image_path):
        image_path = image_path.replace('%20', ' ')

        name, extension = self.get_document_name_and_extension(image_path)
        new_file_name = name + '.pdf'
        pdf_path = os.path.join(MEDIA_ROOT, 'pdf')
        location_path = os.path.join(pdf_path, new_file_name)
        image = Image.open(image_path)
        pdf_bytes = img2pdf.convert(image.filename)
        file = open(location_path, 'wb')
        file.write(pdf_bytes)
        image.close()
        file.close()
        return location_path

    def convert_pdf_to_img(self, pdf_path):
        images = convert_from_path(pdf_path)
        name, extension = self.get_document_name_and_extension(pdf_path)
        image_paths = []
        for counter, img in enumerate(images):
            img.save(name + '_page(' + str(counter) + '.jpg', 'JPEG')
            image_paths.append(img)
        return image_paths


class PowerPoint(Converter):
    pass


class Word(Converter):
    def covert_docx_to_pdf(self, document_path):
        with open(document_path, mode='rb') as f:
            reader = PyPDF2.PdfFileReader(f)
            number_of_pages = reader.numPages
            pdf_text = ''
            for page in range(number_of_pages):
                page_obj = reader.getPage(page)
                pdf_text += page_obj.extractText()
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Arial', size=15)
            pdf.cell(200, 10, txt=pdf_text, ln=1, align='C')
            name, extension = self.get_document_name_and_extension(document_path)
            new_filename = name + '.' + extension
            location_path = os.path.join(MEDIA_ROOT, new_filename)
            pdf.output(location_path)
            return location_path

    def convert_pdf_to_word(self, document_path):
       pass


'''class Excell(Converter):
    def convert_excel_to_pdf(self, document_path):
        path_to_pdf = 'E:\project\documentconverter\static\images\text_emotion.pdf'
        excel = win32com.client.Dispatch("Excel.Application")

        excel.Visible = False
        try:
            print('Start conversion to PDF')

            # Open
            wb = excel.Workbooks.Open(document_path)

            # Specify the sheet you want to save by index. 1 is the first (leftmost) sheet.
            ws_index_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            wb.WorkSheets(ws_index_list).Select()

            # Save
            wb.ActiveSheet.ExportAsFixedFormat(0, path_to_pdf)
            wb.Close()
            excel.Quit()
        except com_error as e:
            print('failed.')
            logging.error(traceback.format_exc())
        else:
            print('Succeeded.')'''


class HTML(Converter):
    def convert_html_to_pdf(self, document_path):
        pdfkit.from_file(document_path, 'E:\project\documentconverter\static\images\sample.pdf')


# object=Converter('E:\project\documentconverter\static\images\image1.png')
# object.convert_img_to_pdf('E:\project\documentconverter\static\images\image1.png')
# object=ImageDocuments()
# object.convert_pdf_to_img('E:\project\documentconverter\static\images\1xbot.pdf')

# object=Word()
# object.covert_docx_to_pdf('E:\project\documentconverter\static\images\CHAPTER.docx')

# object=HTML()
# object.convert_html_to_pdf('E:\project\documentconverter\static\images\index.html')

'''object = Excell()
object.convert_excel_to_pdf('E:\project\documentconverter\static\images\text_emotion.xlsx')
'''
