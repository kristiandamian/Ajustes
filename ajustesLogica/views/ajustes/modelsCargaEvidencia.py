from django.db import models
from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Selecciona un archivo (JPG, PNG)',
        help_text='max. 42 megabytes'
    )
    docfile  = forms.FileField()
    
    def clean_upload(self):
        MAX_UPLOAD_SIZE = 20971520  # 20MB
        docfile = self.cleaned_data["docfile"]
        content_type = docfile.content_type
        if content_type in  ['application/pdf', 'image/jpeg', 'image/png']:
            if docfile._size > MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('el archivo debe ser menor a %s. Intentas subir un archivo de %s')\
                       % (filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(upload._size)))
        else:
            raise forms.ValidationError(_('Ese tipo de archivo no esta soportado'))

        return docfile