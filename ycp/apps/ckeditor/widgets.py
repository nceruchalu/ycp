from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.forms.util import flatatt
import json


class CKEditorWidget(forms.Textarea):
    """
    Description: Widget providing CKEditor for Rich Text Editing
                 Supports direct image uploads and embeds them.
                
    Author:      Nnoduka Eruchalu
    """
    
    class Media:
        js = (settings.STATIC_URL + 'ckeditor/ckeditor.js',)
    
    
    def __init__(self, *args, **kwargs):
        super(CKEditorWidget, self).__init__(*args, **kwargs)
        # setup config from defaults.
        self.config = settings.CKEDITOR_CONFIG.copy()
    
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        
        self.config['filebrowserImageUploadUrl'] = reverse('ckeditorUpload')
        self.config['filebrowserImageBrowseUrl'] = reverse('ckeditorBrowse')
        
        self.config['filebrowserUploadUrl'] = reverse('ckeditorUploadFile')
        self.config['filebrowserBrowseUrl'] = reverse('ckeditorBrowse')
        
        return mark_safe(render_to_string('ckeditor/widget.html', {
                    'final_attrs':flatatt(final_attrs),
                    'value':conditional_escape(force_unicode(value)),
                    'id':final_attrs['id'],
                    'config':json.JSONEncoder().encode(self.config)
                    }))

    
            
