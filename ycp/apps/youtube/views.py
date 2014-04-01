from ycp.apps.youtube.api import Api
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings

from ycp.apps.youtube.models import Video
from ycp.apps.youtube.forms import YoutubeBrowerUploadForm, YoutubeUploadUrlForm, YoutubeEditForm
from ycp.apps.media.models import Media
from ycp.apps.media.forms import MediaEditForm
from ycp.apps.youtube.utils import youtubeParser


# Create your views here.
@login_required
@permission_required('youtube.add_video', login_url=settings.LOGIN_URL)
def uploadBrowser(request):
    """
    See:
    https://developers.google.com/youtube/2.0/developers_guide_protocol#Browser_based_uploading
        
    Steps:
    1. Submit an Upload API request. This request request contains the
       information about the uploaded video file, but does NOT include the
       actual video file. So this includes meta data like title, description,
       category, keywords.
       
    2. Extract values from the API response. The API response contains an upload
       URL and upload token that enable the user to upload the actual video file
       These will have to be included on the webpage where the user submits the
       video file.
    
    3. After extracting the upload URL and upload token from the API response,
       display a form so that the user can upload the actual video file.
       The form must use the upload URL as the value of the <form> tag's action
       attribute and have a hidden input field containing the upload token.
       The form should verify that the user actually has selected a file to
       upload before allowing the user to actually submit the form. [Use JS]
       
    
    Author:      Nnoduka Eruchalu
    """
    if request.method == 'POST':
        # get the metadata
        form = YoutubeBrowerUploadForm(request.POST)
        if form.is_valid():
            # will only create video info after upload finishes
                        
            # try to create post_url and token to create a video upload form
            api = Api()
            # upload method needs authentication
            api.authenticate()
            data = api.uploadBrowser(
                title = form.cleaned_data['title'],
                description = form.cleaned_data['description'],
                keywords = form.cleaned_data['tags'])
            
            protocol = 'https' if request.is_secure() else 'http'
            next_url = '%s://%s%s' % (protocol, request.get_host(),
                                       reverse('youtubeUploadBrowserReturn'))
            # create video upload form
            return render_to_response("youtube/uploadBrowserVideo.html",
                                      {'youtube_token':data['youtube_token'],
                                       'post_url':data['post_url'],
                                       'next_url':next_url
                                       },
                                      context_instance =RequestContext(request))

    # if request.method != 'POST'
    else:
        form = YoutubeBrowerUploadForm()
    
    return render_to_response("youtube/uploadBrowserMeta.html",
                              {'form':form,
                                'nav_current':'file'},
                              context_instance =RequestContext(request))
        

@login_required
@permission_required('youtube.add_video', login_url=settings.LOGIN_URL)
def uploadBrowserReturn(request):
    """
    Description: The upload result page
                 Youtube will redirect to this page after the upload is finished
                 Finally create the video model instance and move on
                 
    Arguments:   -request: HttpRequest object
    Return:      HttpResponse redirecting user to a new page
    
    Author:      Nnoduka Eruchalu
    """
    status = request.GET.get("status")
    video_id = request.GET.get("id")
    
    if status == "200" and video_id:
        # upload is successful
        video = Video()
        video.user = request.user # who is uploading this?
        video.video_id = video_id
        video.save() # this finally creates database record
        video.save() # because tags dont save till save_m2m is called
        messages.add_message(
            request, messages.SUCCESS, "Video successfully uploaded")
        return HttpResponseRedirect(reverse("mediaLibrary"))
    
    else:
        messages.add_message(
            request, messages.ERROR, "Video upload failed")
        return HttpResponseRedirect(reverse("youtubeUploadBrowser"))


@login_required
@permission_required('youtube.add_video', login_url=settings.LOGIN_URL)
def uploadUrl(request):
    """
    Description: Create a video object by specifying a YouTube URL.
                 
    Arguments:   -request: HttpRequest object
    Return:      HttpResponse
    
    Author:      Nnoduka Eruchalu
    """
    if request.method == 'POST':
        form = YoutubeUploadUrlForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            
            # grab video id and indicate this is a url upload
            video.file_upload = False
            video.video_id = youtubeParser(form.cleaned_data['url'])
            
            video.user = request.user # who is uploading this?
            video.save()              # this finally creates database record
            form.save_m2m()           # this is to save tags 
            messages.add_message(
                request, messages.SUCCESS, "Video successfully uploaded")
            return HttpResponseRedirect(reverse("mediaLibrary")) 
        
    # if request.method != 'POST'
    else:
        form = YoutubeUploadUrlForm()
    
    return render_to_response("youtube/uploadBrowserMeta.html",
                              {'form':form,
                                'nav_current':'url'},
                              context_instance = RequestContext(request))
    

@login_required
@permission_required('youtube.add_video', login_url=settings.LOGIN_URL)
def uploadDirect(request):
    """
    See:
    https://developers.google.com/youtube/2.0/developers_guide_protocol#Direct_uploading
    
    Steps:
    1. To upload a video, send a POST request containing the video and metadata.
      
    2. The API returns info about the uploaded video.
    
    Author: Nnoduka Eruchalu
    """
    # will implement when time permits
    return HttpResponseRedirect(reverse("youtubeUploadBrowser"))
    

@login_required
@permission_required('youtube.change_video', login_url=settings.LOGIN_URL)
def edit(request, id):
    """
    Description: Edit given video
                 If edit is successful, return to page with videos with a 
                   success status message
                 If edit isn't succesful, go to the video edit page.
    
    Arguments:   - request: HttpRequest object
                 - id: id of video of interest
    Return:      None
    
    Author:      Nnoduka Eruchalu
    """
    video = get_object_or_404(Video, id=id)
    media = get_object_or_404(Media, video=video)
    
    if request.method == 'POST':
        form = YoutubeEditForm(request.POST, instance=video)
        form2 = MediaEditForm(request.POST, instance=media)
        # use & or all to avoid short-circuiting
        if form.is_valid() & form2.is_valid():
            vid = form.save()
            vid.save() # because tags dont save till save_m2m is called
            media_new = form2.save()
            if media_new.gallery:
                redirect = reverse("mediaGalleryContent",
                                   kwargs={'id':media_new.gallery.id})
            else:
                redirect = reverse("mediaLibrary")
            
            messages.add_message(
                request, messages.SUCCESS, "Video successfully edited")
            return HttpResponseRedirect(redirect)
        
    
    # if request.method != 'POST'
    else:
        form = YoutubeEditForm(instance=video)
        form2 = MediaEditForm(instance=media)
    
    return render_to_response("youtube/edit.html",
                              {'form':form,
                               'form2':form2},
                              context_instance = RequestContext(request))


@login_required
@require_http_methods(["POST"])
@permission_required('youtube.delete_video', login_url=settings.LOGIN_URL)
def delete(request, id):
    """
    Description: Delete given video then return to videos page.
                 A success status message is logged
        
    Arguments:   - request: HttpRequest object
                 - id: id of video of interest
    Return:      None
    
    Author:      Nnoduka Eruchalu
    """
    video = get_object_or_404(Video, id=id)
    media = get_object_or_404(Media, video=video)
    if media.gallery:
        redirect = reverse("mediaGalleryContent",
                           kwargs={'id':media.gallery.id})
    else:
        redirect = reverse("mediaLibrary")
    
    try:
        video.delete()
        messages.add_message(
            request, messages.SUCCESS, "Video successfully deleted")
    except Video.DoesNotExist:
        messages.add_message(
            request, messages.ERROR, "Video couldn't be deleted")
        
    return HttpResponseRedirect(redirect)
