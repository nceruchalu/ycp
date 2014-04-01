from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.core.files.base import ContentFile

from ycp.apps.photo.models import Photo
from ycp.apps.photo.forms import PhotoUploadForm, PhotoUploadUrlForm, PhotoEditForm
from ycp.apps.media.models import Media
from ycp.apps.media.forms import MediaEditForm

import urllib2, urlparse

# Create your views here.
@login_required
@permission_required('photo.add_photo', login_url=settings.LOGIN_URL)
def upload(request):
    """
    Description: upload photo using image file
    
    Arguments:   - request: HttpRequest object
    Return:      HttpResponse
    
    Author:      Nnoduka Eruchalu
    """
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user # who is uploading this?
            photo.save()              # finally create db record
            form.save_m2m()          # this is to save tags
            messages.add_message(
                request, messages.SUCCESS, "Photo successfully uploaded")
            return HttpResponseRedirect(reverse("mediaLibrary"))
            
    else:
        form = PhotoUploadForm()
    
    return render_to_response("photo/upload.html",
                              {'form':form,
                               'nav_current':'file'},
                              context_instance = RequestContext(request))


@login_required
@permission_required('photo.add_photo', login_url=settings.LOGIN_URL)
def uploadUrl(request):
    """
    Description: upload photo using download url
    
    Arguments:   - request: HttpRequest object
    Return:      HttpResponse
    
    Author:      Nnoduka Eruchalu
    """
    if request.method == 'POST':
        form = PhotoUploadUrlForm(request.POST)
        if form.is_valid():
            photo = form.save(commit=False)
            
            # grab image from a URL
            image_url = form.cleaned_data['url']
            image_data = urllib2.urlopen(image_url, timeout=5)
            filename = urlparse.urlparse(
                image_data.geturl()).path.split('/')[-1]
            photo.photo.save(filename, ContentFile(image_data.read()),
                             save=False)
            
            photo.user = request.user # who is uploading this?
            photo.save()              # finally create db record
            form.save_m2m()          # this is to save tags
            messages.add_message(
                request, messages.SUCCESS, "Photo successfully uploaded")
            return HttpResponseRedirect(reverse("mediaLibrary"))
            
    else:
        form = PhotoUploadUrlForm()
    
    return render_to_response("photo/upload.html",
                              {'form':form,
                               'nav_current':'url'},
                              context_instance = RequestContext(request))




@login_required
@permission_required('photo.change_photo', login_url=settings.LOGIN_URL)
def edit(request, id):
    """
    Description: Edit given photo
                 If edit is successful, return to page with photos with a 
                   success status message
                 If edit isn't succesful, go to the photo edit page.
        
    Arguments:   - request: HttpRequest object
                 - id: Photo object of interest
    Return:      HttpResponse
    
    Author:      Nnoduka Eruchalu
    """
    photo = get_object_or_404(Photo, id=id)
    media = get_object_or_404(Media, photo=photo)
        
    if request.method == 'POST':
        form = PhotoEditForm(request.POST, instance=photo)
        form2 = MediaEditForm(request.POST, instance=media)
        # use & or all to avoid short-circuiting
        if form.is_valid() & form2.is_valid():
            form.save()
            media_new = form2.save()
            if media_new.gallery:
                redirect = reverse("mediaGalleryContent",
                                   kwargs={'id':media_new.gallery.id})
            else:
                redirect = reverse("mediaLibrary")
            
            messages.add_message(
                request, messages.SUCCESS, "Photo successfully edited")
            return HttpResponseRedirect(redirect)
    
    # if request.method != 'POST'
    else:
        form = PhotoEditForm(instance=photo)
        form2 = MediaEditForm(instance=media)
    
    return render_to_response("photo/edit.html",
                              {'form':form,
                               'form2':form2},
                              context_instance = RequestContext(request))


@login_required
@require_http_methods(["POST"])
@permission_required('photo.delete_photo', login_url=settings.LOGIN_URL)
def delete(request, id):
    """
    Description: Delete given photo then return to photos page.
                 A success status message is logged
    
    Arguments:   - request: HttpRequest object
                 - id: Photo object of interest
    Return:      HttpResponse
    
    Author:      Nnoduka Eruchalu
    """
    photo = get_object_or_404(Photo, id=id)
    media = get_object_or_404(Media, photo=photo)
    if media.gallery:
        redirect = reverse("mediaGalleryContent",
                           kwargs={'id':media.gallery.id})
    else:
        redirect = reverse("mediaLibrary")
    
    try:
        photo.delete()
        messages.add_message(
            request, messages.SUCCESS, "Photo successfully deleted")
    except Photo.DoesNotExist:
        messages.add_message(
            request, messages.ERROR, "Photo couldn't be deleted")
        
    return HttpResponseRedirect(redirect)

