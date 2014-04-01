# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.conf import settings
from ycp.apps.ckeditor.models import Image, File


@login_required
@require_http_methods(["POST"])
@permission_required('ckeditor.add_image', login_url=settings.LOGIN_URL)
@csrf_exempt
def upload(request):
    """
    Description: Uploads an imagefile and send back its URL to CKEditor
                             
    Arguments:   - request: HttpRequest object
    Return:      HttpResponse containing javascript snippet.
    
    Todo:        Validate uploads
                                  
    Author:      Nnoduka Eruchalu
    """
    # Get the uploaded file from request
    upload = request.FILES['upload']
    
    # save file and copy url
    image = Image.objects.create(image=upload, user=request.user)
    # url = image.get_absolute_url()
    url = image.ckpost.url
    
    return HttpResponse(
        "<script type='text/javascript'>"+
        "window.parent.CKEDITOR.tools.callFunction(%s, '%s');</script>" 
        % (request.GET['CKEditorFuncNum'], url))


@login_required
@require_http_methods(["POST"])
@permission_required('ckeditor.add_image', login_url=settings.LOGIN_URL)
@csrf_exempt
def uploadFile(request):
    """
    Description: Uploads any file and send back its URL to CKEditor
                             
    Arguments:   - request: HttpRequest object
    Return:      HttpResponse containing javascript snippet.
    
    Todo:        create a proper permission system
                 Validate uploads
                                  
    Author:      Nnoduka Eruchalu
    """
    # Get the uploaded file from request
    upload = request.FILES['upload']
    
    # save file and copy url
    f = File.objects.create(file=upload, user=request.user)
    url = f.get_absolute_url()
    
    return HttpResponse(
        "<script type='text/javascript'>"+
        "window.parent.CKEDITOR.tools.callFunction(%s, '%s');</script>" 
        % (request.GET['CKEditorFuncNum'], url))


@login_required
def browse(request):
    """
    Description: Browse 50 most recent images uploaded through ckeditor.
                             
    Arguments:   - request: HttpRequest object
    Return:      HttpResponse with recent images rendered.
    
    Todo:        create a proper permission system
                 Validate uploads
                                  
    Author:      Nnoduka Eruchalu
    """
    images = Image.objects.all()[:50]
    return render_to_response("ckeditor/browse.html",
                              {'images':images},
                              context_instance = RequestContext(request))


