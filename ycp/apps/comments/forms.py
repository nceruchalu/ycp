from django import forms
from django.contrib.comments.forms import CommentForm

class CommentOnlyForm(CommentForm):
    """
    Description: Comment Form where comment-text is the only required field
    
    Author:      Nnoduka Eruchalu
    """
    
    # commenter's name
    name = forms.CharField(label="Name (Optional)", max_length=50,
                           required=False)
    # commenter's email
    email = forms.EmailField(label="Email address (Optional)",
                             help_text="Won't be made public",
                             required=False)
    # commenter's website
    url = forms.URLField(label="URL (Optional)", required=False,
                         widget=forms.TextInput(attrs={'placeholder':
                                                           'http://'})
                         )


