"""
Description:
  Additional Context processor for YCP project

Table Of Contents:
  - site: pass the site domain and URL to the template
  
Author: 
  Nnoduka Eruchalu
"""

from django.conf import settings

def site(request):
    """
    Description: pass the site domain and URL to the template
    
    Arguments:   - request: HttpRequest object
    Return:      Dictionary of context to be passed to template with keys:
                 - SITE_DOMAIN: site's domain (e.g. example.com)
                 - SITE_URL: site's url with protocol (e.g. http://example.com)
    
    Author:      Nnoduka Eruchalu
    """
    return {'SITE_DOMAIN':settings.SITE_DOMAIN,
            'SITE_URL':settings.SITE_URL}
