from django import forms

class ContactForm(forms.Form):
    """
    Description: Contact Form
    
    Author:      Nnoduka Eruchalu
    """
    
    name = forms.CharField(max_length=100, required=True)
    email= forms.EmailField(required=True)
    message = forms.CharField(required=True, widget=forms.Textarea)

