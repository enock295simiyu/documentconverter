from zipfile import ZipFile

from PIL import Image
from pdf2image import convert_from_path
from docx2pdf import convert
import pdfkit
import logging
import traceback
import PyPDF2
import os
import img2pdf
import pdftotree
from documentconverter.settings import MEDIA_ROOT
from fpdf import FPDF
from pdf2docx import parse
import glob
import tqdm


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

        command = 'convert ' + image_path + ' -background white -alpha remove -alpha off ' + name+'convert .'+extension

        os.system(command)
        pdf_path = os.path.join(MEDIA_ROOT, 'pdf')
        location_path = os.path.join(pdf_path, new_file_name)
        image = Image.open(image_path)

        pdf_bytes = img2pdf.convert(image.filename)
        print(location_path)
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
            image_name=name + '_page(' + str(counter) + '.jpg'
            img.save(image_name, 'JPEG')
            image_paths.append(image_name)
        new_filename = name + '.' + 'zip'
        location_path = os.path.join(MEDIA_ROOT, new_filename)
        zipObj=ZipFile(location_path,'w')

        for item in image_paths:
            print(item)
            print(type(item))
            zipObj.write(item)
        zipObj.close()
        return location_path


class PowerPoint(Converter):
    def convert_powerpoint_to_pdf(self,document_path):
        name, extension = self.get_document_name_and_extension(document_path)
        new_filename = name + '.' + 'pdf'
        location_path = os.path.join(MEDIA_ROOT, new_filename)
        command = "unoconv -f pdf -t template.pptx -o " + location_path + ' ' + document_path

        os.system(command)
        return location_path

    def convert_pdf_to_powerpoint(self,document_path):
        name, extension = self.get_document_name_and_extension(document_path)
        new_filename = name + '.' + 'pptx'
        location_path = os.path.join(MEDIA_ROOT, new_filename)

        command = "unoconv -f ppt -t template.pdf -o " + location_path + ' ' + document_path
        os.system(command)
        return location_path



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
            new_filename = name + '.' + 'pdf'
            location_path = os.path.join(MEDIA_ROOT, new_filename)
            pdf.output(location_path)
            return location_path

    def convert_pdf_to_word(self, document_path):
        name, extension = self.get_document_name_and_extension(document_path)
        new_filename = name + '.' + 'docx'
        location_path = os.path.join(MEDIA_ROOT, new_filename)
        parse(document_path,location_path)
        return location_path



class Excell(Converter):
    def convert_excel_to_pdf(self, document_path):
        name, extension = self.get_document_name_and_extension(document_path)
        new_filename = name + '.' + 'pdf'
        location_path = os.path.join(MEDIA_ROOT, new_filename)
        command = "unoconv -f pdf -t template.xls -o "+location_path+' '+document_path
        os.system(command)
        return location_path

    def convert_pdf_to_excell(self,document_path):
        name, extension = self.get_document_name_and_extension(document_path)
        new_filename = name + '.' + 'xls'
        location_path = os.path.join(MEDIA_ROOT, new_filename)
        command = "unoconv -f xls -t template.pdf -o " + location_path + ' ' + document_path
        os.system(command)
        return location_path


class HTML(Converter):
    def convert_html_to_pdf(self, document_path):
        name, extension = self.get_document_name_and_extension(document_path)
        new_filename = name + '.' + 'pdf'
        location_path = os.path.join(MEDIA_ROOT, new_filename)
        pdfkit.from_file(document_path, location_path)
        return location_path

    def convert_pdf_to_html(self,document_path):
        name, extension = self.get_document_name_and_extension(document_path)
        new_filename = name + '.' + 'html'
        location_path = os.path.join(MEDIA_ROOT, new_filename)

        pdftotree.parse(document_path,html_path=location_path,model_type=None,model_path=None,visualize=False)
        return location_path


