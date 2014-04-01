from django import forms
from ycp.apps.media.models import GalleryUpload, Gallery, Media

class GalleryUploadForm(forms.ModelForm):
    """
    Description: Gallery upload form
    
    Author:      Nnoduka Eruchalu
    """
    class Meta:
        model = GalleryUpload


class GalleryEditForm(forms.ModelForm):
    """
    Description: Gallery edit form
    
    Author:      Nnoduka Eruchalu
    """
    class Meta:
        model = Gallery


class MediaEditForm(forms.ModelForm):
    """
    Description: Media Edit Form
    
    Author:      Nnoduka Eruchalu
    """
    class Meta:
        model = Media

