from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings
from django.contrib.comments.models import Comment
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ycp.apps.youtube.models import Video
from ycp.apps.photo.models import Photo
from ycp.apps.media.models import Media, Gallery
from ycp.apps.media.forms import GalleryUploadForm, GalleryEditForm

import json

# Create your views here.

def library(request):
    """
    Description: media library (consists of photos and videos)
    
    Arguments:   - request: HttpRequest object
    Return:      HttpResponse with rendering of library page text
    
    Author:      Nnoduka Eruchalu
    """
    media_list = Media.objects.filter(gallery=None)
    
    paginator = Paginator(media_list, settings.MEDIA_PER_PAGE)
    
    page = request.GET.get('page')
    try:
        media = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page.
        media = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 999), deliver last page of results
        media = paginator.page(paginator.num_pages)
    
    if media.has_next():
        next_page_num = media.next_page_number()
    else:
        next_page_num = 0 # way of indicating no more pages... 1 index'd helped!
    
    if media.has_previous():
        prev_page_num = media.previous_page_number()
    else:
        prev_page_num = 0
        
    media = media.object_list
    
    return render_to_response('media/gallery.html',
                              {'media':media,
                               'nav_current':'library',
                               'next_page':next_page_num,
                               'prev_page':prev_page_num,
                               'addbutton':'media'},
                              context_instance=RequestContext(request))

def gallery(request):
    """
    Description: media galleries
        
    Arguments:   - request: HttpRequest object
    Return:      HttpResponse with rendering of gallery page text
    
    Author:      Nnoduka Eruchalu
    """
    galleries = Gallery.objects.all()
    return render_to_response('media/gallery.html',
                              {'galleries':galleries,
                               'galleries_page':True,
                               'nav_current':'galleries',
                               'expandable_thumbnails':False,
                               'addbutton':'media'},
                              context_instance=RequestContext(request))


def galleryContent(request, id):
    """
    Description: view content of specific gallery
         
    Arguments:   - request: HttpRequest object
                 - id:      id of gallery of interest
    Return:      HttpResponse with rendering of specific gallery content.
    
    Author:      Nnoduka Eruchalu
    """
    gallery = get_object_or_404(Gallery, id=id)
    media_list = gallery.media_set.all()
    
    paginator = Paginator(media_list, settings.MEDIA_PER_PAGE)
    
    page = request.GET.get('page')
    try:
        media = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page.
        media = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 999), deliver last page of results
        media = paginator.page(paginator.num_pages)
    
    if media.has_next():
        next_page_num = media.next_page_number()
    else:
        next_page_num = 0 # way of indicating no more pages... 1 index'd helped!
    
    if media.has_previous():
        prev_page_num = media.previous_page_number()
    else:
        prev_page_num = 0
        
    media = media.object_list
    
    return render_to_response('media/gallery.html',
                              {'media':media,
                               'addbutton':'media',
                               'gallery_id':id,
                               'next_page':next_page_num,
                               'prev_page':prev_page_num,
                               'page_heading':"Gallery: "+ gallery.title},
                              context_instance=RequestContext(request))


def detailPhoto(request, id):
    """
    Description: media Photo detail
         
    Arguments:   - request: HttpRequest object
                 - id:      id of photo of interest
    Return:      JSON HttpResponse with dictionary of a given photo's content.
                 Dictionary has keys:
                 - url:   photo's URL
                 - title: photo title
                 - user:  full name of photo uploader
                 - description: photo's description
                 - comments_html: html representation of comments
                 - tags: list of photo's tags.
    
    Author:      Nnoduka Eruchalu
    """
    photo = get_object_or_404(Photo, id=id)
    comments = Comment.objects.for_model(photo).all().order_by(
        'submit_date')[:5]
    comments_html= render_to_string('comments/list.html',
                                    {'comments':comments},
                                    context_instance=RequestContext(request))
    if request.is_ajax():
        json_response = json.dumps({
                'url':photo.get_absolute_url(),
                'title':photo.title,
                'user':photo.user.get_full_name() or photo.user.get_username(),
                'description':photo.description,
                'comments_html':comments_html,
                'tags':[t.name for t in photo.tags.all()]
                })
        return HttpResponse(json_response, content_type="application/json")
    
    # coming this far isnt legit
    raise Http404


def detailVideo(request, id):
    """
    Description: media Video detail
         
    Arguments:   - request: HttpRequest object
                 - id:      id of video of interest
    Return:      JSON HttpResponse with dictionary of a given video's content.
                 Dictionary has keys:
                 - url:   video's URL
                 - title: video title
                 - user:  full name of video uploader
                 - description: video's description
                 - comments_html: html representation of comments
                 - tags: list of video's tags.
    
    Author:      Nnoduka Eruchalu
    """
    video = get_object_or_404(Video, id=id)
    comments = Comment.objects.for_model(video).all().order_by(
        '-submit_date')[:5]
    comments_html= render_to_string('comments/list.html',
                                    {'comments':comments},
                                    context_instance=RequestContext(request))
    if request.is_ajax():
        json_response = json.dumps({
                'url':video.video_id,
                'title':video.title,
                'user':video.user.get_full_name() or video.user.get_username(),
                'description':video.description,
                'comments_html':comments_html,
                'tags':[t.name for t in video.tags.all()]
                })
        return HttpResponse(json_response, content_type="application/json")
    
    # coming this far isnt legit
    raise Http404


def mediaDetail(request, id):
    """
    Description: details of media on a page of its own
         
    Arguments:   - request: HttpRequest object
                 - id:      id of media of interest
    Return:      JSON HttpResponse with dictionary of a given media's content.
                     
    Author:      Nnoduka Eruchalu
    """
    media = get_object_or_404(Media, id=id)
    comments_list = Comment.objects.for_model(media.object()).all().order_by(
        'submit_date')
    paginator = Paginator(comments_list, settings.COMMENTS_PER_PAGE)
    
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page.
        comments = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 999), deliver last page of results
        comments = paginator.page(paginator.num_pages)
    
    if comments.has_next():
        next_page_num = comments.next_page_number()
    else:
        next_page_num = 0 # way of indicating no more pages... 1 index'd helped!
    
    comments = comments.object_list
    
    comments_html= render_to_string('comments/list-contents.html',
                                    {'comments':comments},
                                    context_instance=RequestContext(request))
    
    if request.is_ajax(): # the only way more comments should be loaded
        json_response = json.dumps({
                'next_page': next_page_num,
                'comments_html': comments_html,
                })
        return HttpResponse(json_response, content_type="application/json")
    
    # get next and previous media items within same gallery
    try:
        next_media = media.get_next_by_created(gallery=media.gallery)
    except Media.DoesNotExist:
        next_media = False
    
    try:
        prev_media = media.get_previous_by_created(gallery=media.gallery)
    except Media.DoesNotExist:
        prev_media = False
    
    return render_to_response('media/mediaDetail.html',
                              {'media':media,
                               'comments':comments,
                               'next_page':next_page_num,
                               'next_media':next_media,
                               'prev_media':prev_media,
                               'addbutton':'media'},
                              context_instance=RequestContext(request))


@login_required
@permission_required('media.add_gallery', login_url=settings.LOGIN_URL)
@permission_required('photo.add_photo', login_url=settings.LOGIN_URL)
def uploadZip(request):
    """
    Description: Upload zip file to a gallery
    
    Arguments:   - request: HttpRequest object
    Return:      HttpResponse
    
    Author:      Nnoduka Eruchalu
    """
    # if a POST request, then this is a form submission attempt
    if request.method == 'POST':
        form = GalleryUploadForm(request.POST, request.FILES)
        if form.is_valid():
            galleryUpload = form.save(commit=False)
            galleryUpload.user = request.user # who is uploading this?
            gallery = galleryUpload.save()
            messages.add_message(
                request, messages.SUCCESS, "Gallery Zip successfully uploaded")
            return HttpResponseRedirect(reverse("mediaGalleryContent",
                                                kwargs={'id':gallery.id}))
    
    # if a GET request, show upload form
    else:
        form = GalleryUploadForm()
    
    return render_to_response("media/gallery/upload.html",
                              {'form':form},
                              context_instance = RequestContext(request))


@login_required
@permission_required('media.add_gallery', login_url=settings.LOGIN_URL)
def galleryCreate(request):
    """
    Description: Create gallery, go to gallery page
    
    Arguments:   - request: HttpRequest object
    Return:      HttpResponse
    
    Author:      Nnoduka Eruchalu
    """
    if request.method == 'POST':
        form = GalleryEditForm(request.POST)
        if form.is_valid():
            gallery = form.save(commit=False)
            gallery.user = request.user # who is uploading this?
            gallery.save()              # finally create db record
            messages.add_message(
                request, messages.SUCCESS, "Gallery successfully created")
            return HttpResponseRedirect(reverse("mediaGallery"))
            
    else:
        form = GalleryEditForm()
    
    return render_to_response("media/gallery/edit.html",
                              {'form':form},
                              context_instance = RequestContext(request))


@login_required
@permission_required('media.change_gallery', login_url=settings.LOGIN_URL)
def galleryEdit(request, id):
    """
    Description: Edit given gallery, return to gallery page
    
    Arguments:   - request: HttpRequest object
                 - id:      id of gallery of interest
    Return:      HttpResponse
    
    Author:      Nnoduka Eruchalu
    """
    gallery = get_object_or_404(Gallery, id=id)
    
    if request.method == 'POST':
        form = GalleryEditForm(request.POST, instance=gallery)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "Gallery successfully edited")
            
            return HttpResponseRedirect(reverse("mediaGalleryContent",
                                                kwargs={'id':id}))
    
    # if request.method != 'POST'
    else:
        form = GalleryEditForm(instance=gallery)
    
    return render_to_response("media/gallery/edit.html",
                              {'form':form},
                              context_instance = RequestContext(request))


@login_required
@require_http_methods(["POST"])
@permission_required('media.delete_gallery', login_url=settings.LOGIN_URL)
def galleryDelete(request, id):
    """
    Description: Delete given gallery then return to gallery page.
                 A success status message is logged
    
    Arguments:   - request: HttpRequest object
                 - id:      id of gallery of interest
    Return:      HttpResponse
    
    Author:      Nnoduka Eruchalu
    """
    redirect = reverse("mediaGallery")
    
    try:
        Gallery.objects.get(id=id).delete()
        messages.add_message(
            request, messages.SUCCESS, "Gallery successfully deleted")
    except Photo.DoesNotExist:
        messages.add_message(
            request, messages.ERROR, "Gallery couldn't be deleted")
        
    return HttpResponseRedirect(redirect)

