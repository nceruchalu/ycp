"""
Description:
  Utility functions that come in handy through the project

Table Of Contents:
  - slugify:         slugify any given string
  - get_upload_path: determine a unique upload path for a given file
  
Author: 
  Nnoduka Eruchalu
"""

from datetime import datetime
import os, re, unicodedata

#imports for pagination
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def slugify(string):
    """
    Description: Slugify any given string with following rules:
                 - ASCII encoding
                 - Non-alphanumerics are replaced with hyphens
                 - groups of hyphens will be replaced with a single hyphen
                 - slugs cannot begin/end with hyphens.
    
    Arguments:   - string: string to get slugged version of
    Return:      ASCII slugified version of input string
        
    Author:      Nnoduka Eruchalu
    """
    s = unicode(string)
    slug = unicodedata.normalize('NFKD', s)
    slug = slug.encode('ascii', 'ignore').lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    slug = re.sub(r'[-]+', '-', slug)
    return slug


def get_upload_path(instance, filename, root):
    """
    Description: Determine a unique upload path for a given file
    
    Arguments:   - instance: model instance where the file is being attached
                 - filename: filename that was originally given to the file
                 - root:     root folder to be prepended to file upload path.
                             Example value is 'photo/' or 'photo'  
    Return:      Unique filepath for given file, that's a subpath of `root`
            
    Author:      Nnoduka Eruchalu
    """
    name = filename.split('.')
    format = slugify(name[0])+"_"+ str(datetime.now().strftime("%Y%m%dT%H%M%S")) + "." + name[len(name)-1]
    return os.path.join(root, format)

