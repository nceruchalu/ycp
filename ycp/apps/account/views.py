from django.shortcuts import redirect
from django.contrib.auth.views import login
from django.contrib.auth.views import login
from django.conf import settings
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

@sensitive_post_parameters()
@csrf_protect
@never_cache
def custom_login(request, **kwargs):
    """    
    Description: Custom login view handler where a user is not sent to login
                 view if already authenticated. An authenticated user is taken
                 straight to the LOGIN_REDIRECT_URL page.
                   
    Arguments:   - request: HttpRequest object
                 - **kwargs
    Return:      HttpResponse 
    
    Author:      Nnoduka Eruchalu
    """
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL, **kwargs)
    else:
        return login(request, **kwargs)

