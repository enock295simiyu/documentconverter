import mimetypes
import os

from PIL import Image
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import urlencode
import ntpath

from pdf2image import convert_from_path

# Create your views here.


# Create your views here.
from core.forms import DocumentForm
from core.main import ImageDocuments, Word
from documentconverter.settings import BASE_DIR


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

        return final_url


def pdf_to_jpg(request):
    if request.method == 'POST':
        upload_file_url = upload_document(request)

        document = ImageDocuments()
        image_path = document.convert_pdf_to_img(upload_file_url)
        print(image_path)

    template = 'upload.html'

    return render(request, template)


def pdf_to_word(request):
    if request.method=='POST':
        upload_file_url = upload_document(request)
        document=Word()

    template = 'upload.html'
    return render(request, template)


def pdf_to_pptx(request):
    upload_file_url = upload_document(request)
    template = 'upload.html'
    return render(request, template)


def pdf_to_html(request):
    upload_file_url = upload_document(request)
    template = 'upload.html'
    return render(request, template)


def jpg_to_pdf(request):
    if request.method == 'POST':

        upload_file_url = upload_document(request)

        document = ImageDocuments()
        image_path = document.convert_img_to_pdf(upload_file_url)

        download_base=reverse('download')
        query_string=urlencode({'file_url':image_path})
        url='{}?{}'.format(download_base,query_string)
        return redirect(url)

    template = 'upload.html'
    return render(request, template)


def word_to_pdf(request):
    if request.method=='POST':
        upload_file_url=upload_document(request)
        document=Word()
        new_document_path=document.covert_docx_to_pdf(upload_file_url)
        download_base=reverse('download')
        query_string=urlencode({'file_url':new_document_path})
        url='{}?{}'.format(download_base,query_string)
        return redirect(url)
    template = 'upload.html'
    return render(request, template)


def pptx_to_pdf(request):
    upload_file_url = upload_document(request)
    template = 'upload.html'
    return render(request, template)


def html_to_pdf(request):
    upload_file_url = upload_document(request)
    template = 'upload.html'
    return render(request, template)


def excel_to_pdf(request):
    upload_file_url = upload_document(request)
    template = 'upload.html'
    return render(request, template)


def pdf_to_excel(request):
    upload_file_url = upload_document(request)
    template = 'upload.html'
    return render(request, template)


def download_document(request):
    file_location=request.GET.get('file_url')
    file_name=ntpath.basename(file_location)
    with open(file_location,'rb') as fh:
        mime_type,_=mimetypes.guess_type(file_location)

        response=HttpResponse(fh.read(),content_type=mime_type)
        response['Content-Disposition']='attachment;filename=%s'%file_name
        return response

