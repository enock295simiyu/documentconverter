from django.db import models

# Create your models here.

type_choices = (('pdf', 'pdf'), ('image', 'image'), ('word', 'word'), ('powerpoint', 'powerpoint'), ('excel', 'excel'),
                ('html', 'html'))



class Document(models.Model):
    type = models.CharField(max_length=100,choices=type_choices)
    name = models.CharField(max_length=500, null=True, blank=True)
    document = models.FileField(upload_to='documents/',blank=True,null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
