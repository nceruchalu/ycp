# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from ycp.apps.staticpage.forms import ContactForm
from django.core.mail import EmailMessage
from django.conf import settings


def direct_to_template(request, template, kwargs=None):
    """
    Description: contact form page
    
    Arguments:   - request: HttpRequest object
                 - template to be rendered
                 - kwargs: context to be used when rendering template
    Return:      HttpResponse with rendered template text
    
    Author:      Nnoduka Eruchalu
    """
    return render_to_response(template, kwargs,
                              context_instance=RequestContext(request))


def contact(request):
    """
    Description: contact form page
    
    Arguments:   - request: HttpRequest object
    Return:      HttpResponse
    
    Author:      Nnoduka Eruchalu
    """
    success = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            body = "Name: "+cd['name']+"\nEmail: "+cd['email']+\
                "\n\nMessage:\n"+cd['message']
            subject = "email from "+settings.SITE_DOMAIN+" contact form"
            email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL,
                                 [settings.CONTACT_EMAIL],
                                 headers={'Reply-To':cd['email']})
            email.send(fail_silently=True)
            
            form = ContactForm() # clear contact form
            success = True # to display "thank you" message
    else:
        form = ContactForm()
    
    return render_to_response('staticpage/about/contact.html',
                              {'form': form, 
                               'success': success,
                               'currentnav':'contact'},
                              context_instance=RequestContext(request))

