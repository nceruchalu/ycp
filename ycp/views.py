from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from ycp.apps.photo.models import Photo
from ycp.apps.blog.models import Post

from haystack.forms import SearchForm
from haystack.query import EmptySearchQuerySet

def homepage(request):
    """
    Description: Render YCP's home page
    
    Arguments:   - request: HttpRequest object
    Return:      HttpResponse object with rendered text of home page
        
    Author:      Nnoduka Eruchalu
    """
    photos = Photo.objects.all()[:5]
    posts = Post.objects.all()[:3]
    return render_to_response('home/home.html',
                              {'pagetype':'homepage',
                               'photos':photos,
                               'posts':posts},
                              context_instance=RequestContext(request))


def search(request):
    """
    Description: Handles requests from site's search bar
                 Based off haystack.views.basic_search()
                   
    Arguments:   request: HttpRequest object
    Return:      HttpResponse object showing search results with following 
                 additional details
                 - query:      search query
                 - suggestion: backend-suggested search query
    
    Author:      Nnoduka Eruchalu
    """
    query = ''
    results = EmptySearchQuerySet()
    suggestion = False
    
    if request.GET.get('q'):
        form = SearchForm(request.GET, searchqueryset=None, load_all=True)
        if form.is_valid():
            query = form.cleaned_data['q']
            results = form.search()
        
        if results.query.backend.include_spelling:
            suggestion = form.get_suggestion()
        
                    
    search_list = [r.object for r in results]
    
    paginator = Paginator(search_list, settings.RESULTS_PER_PAGE)
    
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
    
    return render_to_response('search/search.html',
                              {'query':query,
                               'suggestion':suggestion,
                               'results':results,
                               'next_page':next_page_num,
                               'prev_page':prev_page_num},
                              context_instance=RequestContext(request))


def opensearch(request):
    """
    Description: Serve opensearch.xml file
    
    Arguments:   - request: HttpRequest object
    Return:      HttpResponse object with rendered opensearch.xml content 
      
    Author:      Nnoduka Eruchalu
    """
    return render_to_response('opensearch.xml',
                              context_instance=RequestContext(request),
                              content_type="application/xhtml+xml")
