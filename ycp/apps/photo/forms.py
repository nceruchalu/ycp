from django import forms
from ycp.apps.photo.models import Photo
import urllib2, cStringIO

try:
    from PIL import Image
except ImportError:
    import Image

class PhotoUploadForm(forms.ModelForm):
    """
    Description: Photo upload form using image file
    
    Author:      Nnoduka Eruchalu
    """
    class Meta:
        model = Photo


class PhotoUploadUrlForm(forms.ModelForm):
    """
    Description: Photo upload form by entering a url
    
    Author:      Nnoduka Eruchalu
    """
    url = forms.URLField(label="URL")
    
    class Meta:
        model = Photo
        fields = ('title', 'description','url','tags',)
        exclude = ('photo',)
       
        
    def clean_url(self):
        url = self.cleaned_data['url']
                
        try:
            data = urllib2.urlopen(url, timeout=5)
            data_file = cStringIO.StringIO(data.read())
            # load() could spot a truncated JPEG, but it loads the entire
            # image in memory, which is a DoS vector. See #3848 and #18520.
            # verify() must be called immediately after the constructor.
            Image.open(data_file).verify()
        except ImportError:
            # Under PyPy, it is possible to import PIL. However, the underlying
            # _imaging C module isn't available, so an ImportError will be
            # raised. Catch and re-raise.
            raise
        except Exception: 
            # Python Imaging Library doesn't recognize it as an image
            raise forms.ValidationError('invalid image')
                        
        
        # always return the cleaned data, whether you have changed it or not
        return url


class PhotoEditForm(forms.ModelForm):
    """
    Description: Photo edit form
    
    Author:      Nnoduka Eruchalu
    """
    class Meta:
        model = Photo
        exclude = ('photo',)

