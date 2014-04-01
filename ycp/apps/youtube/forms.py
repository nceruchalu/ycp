from django import forms
from ycp.apps.youtube.models import Video
from ycp.apps.youtube.utils import youtubeParser


class YoutubeBrowerUploadForm(forms.ModelForm):
    """
    Description: YouTube's Browser-based upload form (metadata only)
    
    Author:      Nnoduka Eruchalu
    """
    
    class Meta:
        model = Video
        exclude = ('video_file',)


class YoutubeDirectUploadForm(forms.ModelForm):
    """
    Description: YouTube's Direct upload form
    
    Author:      Nnoduka Eruchalu
    """
    
    class Meta:
        model = Video


class YoutubeUploadUrlForm(forms.ModelForm):
    """
    Description: Video upload form by entering a YouTube url
    
    Author:      Nnoduka Eruchalu
    """
    
    url = forms.URLField(label="URL", help_text="Has to be a YouTube URL.")
        
    class Meta:
        model = Video
        fields = ('url', 'title', 'description', 'tags',)
    
    def __init__(self, *args, **kwargs):
        super(YoutubeUploadUrlForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['description'].required = False
        
        self.fields['title'].help_text = \
            "Leave blank to use YouTube video's title."
        self.fields['description'].help_text = \
            "Leave blank to use YouTube video's description."
        self.fields['tags'].help_text = 'A comma-separated list of tags.'
        
        
    def clean_url(self):
        url = self.cleaned_data['url']
        
        if not youtubeParser(url):
            raise forms.ValidationError('invalid YouTube URL')
        
        # always return the cleaned data, whether you have changed it or not
        return url


class YoutubeEditForm(forms.ModelForm):
    """
    Description: YouTube video edit form
    
    Author:      Nnoduka Eruchalu
    """
    class Meta:
        model = Video
        exclude = ('video_file',)
