from django.urls import path
from .views import home, success, jpg_to_pdf, word_to_pdf, html_to_pdf, excel_to_pdf, pptx_to_pdf, pdf_to_jpg, \
    pdf_to_word, pdf_to_pptx, pdf_to_html, pdf_to_excel, download_document

urlpatterns = [
    path('', home, name='home'),
    path('success', success, name='success'),
    path('jpg_to_pdf', jpg_to_pdf, name='jpg_to_pdf'),
    path('word_to_pdf', word_to_pdf, name='word_to_pdf'),
    path('html_to_pdf', html_to_pdf, name='html_to_pdf'),
    path('excel_to_pdf', excel_to_pdf, name='excel_to_pdf'),
    path('pptx_to_pdf', pptx_to_pdf, name='pptx_to_pdf'),
    path('pdf_to_jpg', pdf_to_jpg, name='pdf_to_jpg'),
    path('pdf_to_word', pdf_to_word, name='pdf_to_word'),
    path('pdf_to_pptx', pdf_to_pptx, name='pdf_to_pptx'),
    path('pdf_to_html', pdf_to_html, name='pdf_to_html'),
    path('pdf_to_excel', pdf_to_excel, name='pdf_to_excel'),
    path('download', download_document, name='download'),
]
