from django.db import models
from django import forms

from ycp.apps.ckeditor.widgets import CKEditorWidget

class RichTextField(models.TextField):
    """
    Description: Model Field to be used to represent content edited via 
                 CKEditor's WYSIWYG editor
    
    Author:      Nnoduka Eruchalu
    """
    
    def __init__(self, *args, **kwargs):
        super(RichTextField, self).__init__(*args, **kwargs)
    
    def formfield(self, **kwargs):
        defaults = {
            'form_class': RichTextFormField,
            }
        defaults.update(kwargs)
        return super(RichTextField, self).formfield(**defaults)

class RichTextFormField(forms.fields.Field):
    """
    Description: Form field to be use when displaying content edited via
                 CKEditor in a form.
    
    Author:      Nnoduka Eruchalu
    """
    
    def __init__(self, *args, **kwargs):
        kwargs.update({'widget': CKEditorWidget()})
        super(RichTextFormField, self).__init__(*args, **kwargs)
    
