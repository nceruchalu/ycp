from django import forms
from ycp.apps.blog.models import Post

class PostForm(forms.ModelForm):
    """
    Description: Blog Post edit/create form
    
    Author:      Nnoduka Eruchalu
    """
    class Meta:
        model = Post
        exclude = ('created',)

