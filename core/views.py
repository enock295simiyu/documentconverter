import mimetypes
import os
from io import StringIO

from PIL import Image
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import urlencode
import ntpath
from zipfile import ZipFile
from django.contrib import messages




# Create your views here.


# Create your views here.
from core.forms import DocumentForm
from core.main import ImageDocuments, Word, HTML, PowerPoint, Excell
from documentconverter.settings import BASE_DIR


def validate_file_extension(extension:str,filename:str):
    if filename.endswith(extension):
        return True
    else:
        return False

def home(request):
    template = 'index.html'
    return render(request, template, )


def success(request):
    return HttpResponse('successfully uploaded')


def upload_document(request):
    if request.method == 'POST' and request.FILES['document']:
        myfile = request.FILES['document']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        correct_path=os.path.normpath(uploaded_file_url)
        final_url = os.path.join(BASE_DIR, correct_path[1:])
        final_url=final_url.replace('%20',' ')

        return final_url

def wrong_file_uploaded(request):
    pass

def pdf_to_jpg(request):
    if request.method == 'POST':


        upload_file_url = upload_document(request)
        extension = '.pdf'
        is_extension_correct = validate_file_extension(extension,upload_file_url )
        if is_extension_correct:

            document = ImageDocuments()
            image_path = document.convert_pdf_to_img(upload_file_url)
            download_base = reverse('download')
            query_string = urlencode({'file_url': image_path})
            url = '{}?{}'.format(download_base, query_string)
            return redirect(url)
        else:
            messages.success(request, 'Incorrect file format. The only file accepted ends with .pdf')
            return redirect('/pdf_to_jpg')

    template = 'upload.html'

    return render(request, template)


def pdf_to_word(request):
    if request.method=='POST':
        upload_file_url = upload_document(request)
        extension='.pdf'
        is_extension_correct = validate_file_extension(extension, upload_file_url)
        if is_extension_correct:
            document=Word()
            image_path=document.convert_pdf_to_word(upload_file_url)
            download_base = reverse('download')
            query_string = urlencode({'file_url': image_path})
            url = '{}?{}'.format(download_base, query_string)
            return redirect(url)
        else:
            messages.success(request, 'Incorrect file format. The only file accepted ends with .pdf')
            return redirect('/pdf_to_word')

    template = 'upload.html'
    return render(request, template)


def pdf_to_pptx(request):
    if request.method=='POST':
        upload_file_url=upload_document(request)
        extension = '.pdf'
        is_extension_correct = validate_file_extension(extension, upload_file_url)
        if is_extension_correct:
            document=PowerPoint()
            image_path=document.convert_pdf_to_powerpoint(upload_file_url)
            download_base = reverse('download')
            query_string = urlencode({'file_url': image_path})
            url = '{}?{}'.format(download_base, query_string)
            return redirect(url)
        else:
            messages.success(request, 'Incorrect file format. The only file accepted ends with .pdf')
            return redirect('/pdf_to_pptx')

    template = 'upload.html'
    return render(request, template)


def pdf_to_html(request):
    if request.method=='POST':

        upload_file_url = upload_document(request)
        extension = '.pdf'
        is_extension_correct = validate_file_extension(extension, upload_file_url)
        if is_extension_correct:
            document=HTML()
            image_path=document.convert_pdf_to_html(upload_file_url)
            download_base = reverse('download')
            query_string = urlencode({'file_url': image_path})
            url = '{}?{}'.format(download_base, query_string)
            return redirect(url)
        else:
            messages.success(request, 'Incorrect file format. The only file accepted ends with .pdf')
            return redirect('/pdf_to_html')

    template = 'upload.html'
    return render(request, template)


def jpg_to_pdf(request):
    if request.method == 'POST':

        upload_file_url = upload_document(request)
        extension = '.jpg'
        is_extension_correct = validate_file_extension(extension, upload_file_url)
        if is_extension_correct:

            document = ImageDocuments()
            image_path = document.convert_img_to_pdf(upload_file_url)

            download_base=reverse('download')
            query_string=urlencode({'file_url':image_path})
            url='{}?{}'.format(download_base,query_string)
            return redirect(url)
        else:
            messages.success(request, 'Incorrect file format. The only file accepted ends with .jpg')
            return redirect('/pdf_to_jpg')

    template = 'upload.html'
    return render(request, template)


def word_to_pdf(request):
    if request.method=='POST':
        upload_file_url=upload_document(request)
        extension = '.docx'
        is_extension_correct = validate_file_extension(extension, upload_file_url)
        if is_extension_correct:
            document=Word()
            new_document_path=document.covert_docx_to_pdf(upload_file_url)
            download_base=reverse('download')
            query_string=urlencode({'file_url':new_document_path})
            url='{}?{}'.format(download_base,query_string)
            return redirect(url)
        else:
            messages.success(request, 'Incorrect file format. The only file accepted ends with .docx')
            return redirect('/pdf_to_jpg')
    template = 'upload.html'
    return render(request, template)


def pptx_to_pdf(request):
    if request.method=='POST':
        upload_file_url = upload_document(request)
        extension = '.pptx'
        is_extension_correct = validate_file_extension(extension, upload_file_url)
        if is_extension_correct:
            document = PowerPoint()
            new_document_path = document.convert_powerpoint_to_pdf(upload_file_url)
            download_base = reverse('download')
            query_string = urlencode({'file_url': new_document_path})
            url = '{}?{}'.format(download_base, query_string)
            return redirect(url)
        else:
            messages.success(request, 'Incorrect file format. The only file accepted ends with .pptx')
            return redirect('/pdf_to_jpg')

    template = 'upload.html'
    return render(request, template)


def html_to_pdf(request):
    upload_file_url = upload_document(request)
    template = 'upload.html'
    return render(request, template)


def excel_to_pdf(request):
    if request.method=='POST':

        upload_file_url = upload_document(request)
        extension = '.xls'
        is_extension_correct = validate_file_extension(extension, upload_file_url)
        if is_extension_correct:
            document=Excell()
            new_document_path=document.convert_excel_to_pdf(upload_file_url)
            download_base = reverse('download')
            query_string = urlencode({'file_url': new_document_path})
            url = '{}?{}'.format(download_base, query_string)
            return redirect(url)
        else:
            messages.success(request, 'Incorrect file format. The only file accepted ends with .xsl')
            return redirect('/pdf_to_jpg')

    template = 'upload.html'
    return render(request, template)


def pdf_to_excel(request):
    if request.method == 'POST':
        upload_file_url = upload_document(request)
        extension = '.pdf'
        is_extension_correct = validate_file_extension(extension, upload_file_url)
        if is_extension_correct:
            document = Excell()
            new_document_path = document.convert_pdf_to_excell(upload_file_url)
            download_base = reverse('download')
            query_string = urlencode({'file_url': new_document_path})
            url = '{}?{}'.format(download_base, query_string)
            return redirect(url)
        else:
            messages.success(request, 'Incorrect file format. The only file accepted ends with .pdf')
            return redirect('/pdf_to_jpg')
    template = 'upload.html'
    return render(request, template)


def download_document(request):
    file_location=request.GET.get('file_url')
    file_name=ntpath.basename(file_location)
    file_location=file_location.replace('%20',' ')
    with open(file_location,'rb') as fh:
        mime_type,_=mimetypes.guess_type(file_location)

        response=HttpResponse(fh.read(),content_type=mime_type)
        response['Content-Disposition']='attachment;filename=%s'%file_name
        return response

