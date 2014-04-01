# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from ycp.apps.photo.models import Photo
from ycp.apps.youtube.models import Video
from ycp.apps.blog.models import Post

from itertools import chain
from operator import attrgetter


def details(request, tag):
    """
    Description:  Show the post and media objects that match a given tag.
                                               
    Arguments:   - request: HttpRequest object
                 - tag:     name of desired tag
    Return:      HttpResponse rendering results of objects with matchign tag.
                                  
    Author:      Nnoduka Eruchalu
    """
    posts = Post.objects.filter(tags__name__in=[tag])
    photos = Photo.objects.filter(tags__name__in=[tag])
    videos = Video.objects.filter(tags__name__in=[tag])
    
    results_list = sorted(
        chain(posts, photos, videos),
        key=attrgetter('created'),
        reverse=True
        )
    
    
    paginator = Paginator(results_list, settings.RESULTS_PER_PAGE)
    
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page.
        results = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 999), deliver last page of results
        results = paginator.page(paginator.num_pages)
    
    if results.has_next():
        next_page_num = results.next_page_number()
    else:
        next_page_num = 0 # way of indicating no more pages... 1 index'd helped!
    
    if results.has_previous():
        prev_page_num = results.previous_page_number()
    else:
        prev_page_num = 0
        
    results = results.object_list
    
    return render_to_response('tag/details.html',
                              {'tag':tag,
                               'results':results,
                               'next_page':next_page_num,
                               'prev_page':prev_page_num},
                              context_instance=RequestContext(request))

