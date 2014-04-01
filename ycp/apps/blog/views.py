# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.contrib import messages
from django.contrib.comments.models import Comment
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ycp.apps.blog.models import Post
from ycp.apps.blog.forms import PostForm
import json, datetime


def posts_helper(request, posts_list, nav_current=None, additional_title=None):
    """
    Description: Paginate a list of Song objects, generate the properly
                 formatted response object and return it as a json HttpResponse
                 - see songs_helper_json
                 
    Arguments:   - request:          HttpRequest object
                 - posts_list:       List of Post objects
                 - nav_current:      String to be used for navigation
                 - additional_title: Page sub-title 
    Return:      HttpResponse with list of posts rendered
                 
    Author:      Nnoduka Eruchalu
    """
    paginator = Paginator(posts_list, settings.POSTS_PER_PAGE)
    
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 999), deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
    if posts.has_next():
        next_page_num = posts.next_page_number()
    else:
        next_page_num = 0 # way of indicating no more pages... 1 index'd helped!

    if posts.has_previous():
        prev_page_num = posts.previous_page_number()
    else:
        prev_page_num = 0

    posts = posts.object_list
    
    return render_to_response('blog/posts.html',
                              {'posts':posts,
                               'next_page':next_page_num,
                               'prev_page':prev_page_num,
                               'addbutton':'blog',
                               'nav_current':nav_current,
                               'additional_title':additional_title},
                              context_instance=RequestContext(request))

def posts(request):
    """
    Description: Page of YCP posts
    
    Arguments:   - request: HttpRequest object
    Return:      HttpResponse
                                  
    Author:      Nnoduka Eruchalu
    """
    posts_list = Post.objects.filter(is_public=True)
    return posts_helper(request, posts_list, "posts")


def postDetail(request, id):
    """
    Description:  Show a specific-post page or load its comments.
                                               
    Arguments:   - request: HttpRequest object
                 - id:      id of desired post
    Return:      HttpResponse
                 - For an Ajax request, return the rendered comments text
                 - For a non-ajax request, return post details page.
                                  
    Author:      Nnoduka Eruchalu
    """
    post = get_object_or_404(Post, id=id)
    
    if (not post.is_public) and (post.user != request.user):
        raise Http404
        
    comments_list = Comment.objects.for_model(post).all().order_by(
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
    
    # get next and previous post items
    try:
        next_post = post.get_next_by_created()
    except Post.DoesNotExist:
        next_post = False
    
    try:
        prev_post = post.get_previous_by_created()
    except Post.DoesNotExist:
        prev_post = False
    
    return render_to_response('blog/postDetail.html',
                              {'post':post,
                               'comments':comments,
                               'next_page':next_page_num,
                               'next_post':next_post,
                               'prev_post':prev_post,
                               'addbutton':'blog'},
                              context_instance=RequestContext(request))


def archives(request):
    """
    Description: Page of YCP post archives
    
    Arguments:   - request: HttpRequest object
    Return:      HttpResponse
                                  
    Author:      Nnoduka Eruchalu
    """
    # get post years
    years = Post.objects.filter(is_public=True).dates(
        'created','year', order='DESC')
    
    # get post months and corresponding posts
    months_dates_list = Post.objects.filter(is_public=True).dates(
        'created','month', order='DESC')
    
    paginator = Paginator(months_dates_list, settings.ARCHIVES_MONTHS_PER_PAGE)
    
    page = request.GET.get('page')
    try:
        months_dates = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page.
        months_dates = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 999), deliver last page of results
        months_dates = paginator.page(paginator.num_pages)
    
    if months_dates.has_next():
        next_page_num = months_dates.next_page_number()
    else:
        next_page_num = 0 # way of indicating no more pages... 1 index'd helped!
        
    if months_dates.has_previous():
        prev_page_num = months_dates.previous_page_number()
    else:
        prev_page_num = 0
    
    months_dates = months_dates.object_list
    
    
    months_posts = []
    for d in months_dates:
        months_posts.append(
            Post.objects.filter(is_public=True, created__year=d.year).filter(
                created__month = d.month)
            )
    months = zip(months_dates, months_posts)
    
    # render
    return render_to_response('blog/postArchives.html',
                              {'nav_current':'archives',
                               'years':years,
                               'months':months,
                               'next_page':next_page_num,
                               'prev_page':prev_page_num,
                               'addbutton':'blog'},
                              context_instance=RequestContext(request))


def archivesYear(request, year):
    """
    Description: Page of YCP post archives for a given year
    
    Arguments:   - request: HttpRequest object
                 - year: Year to narrow archives down to
    Return:      HttpResponse
                                  
    Author:      Nnoduka Eruchalu
    """
    # get post months and corresponding posts
    try:
        year = int(year)
        months_dates = Post.objects.filter(is_public=True, created__year=year).dates(
            'created','month', order='DESC') 
        months = []
        
        if months_dates: 
            months_posts = []
            for d in months_dates:
                months_posts.append(
                Post.objects.filter(is_public=True,created__year=d.year).filter(
                        created__month = d.month)
                )
            months = zip(months_dates, months_posts)
            
    except:
        raise Http404
    
    if months:
        # render
        return render_to_response('blog/postArchivesYear.html',
                                  {'year':year,
                                   'months':months},
                                  context_instance=RequestContext(request))
    
    raise Http404


def archivesMonth(request, year, month):
    """
    Description: Page of YCP post archives for a given year and month
    
    Arguments:   - request: HttpRequest object
                 - year: Year to narrow archives down to
                 - month: Month in given year to narrow archives down to
    Return:      HttpResponse
                                  
    Author:      Nnoduka Eruchalu
    """
    # get posts
    try:
        year = int(year)
        month = int(month)
        
        posts = Post.objects.filter(is_public=True, created__year=year).filter(
            created__month=month)
        date = datetime.datetime(year, month, 01)
    except:
        raise Http404
    
    if posts:
        return render_to_response('blog/postArchivesMonth.html',
                                  {'posts':posts,
                                   'date':date},
                                  context_instance=RequestContext(request))
    
    raise Http404


@login_required
@permission_required('blog.add_post', login_url=settings.LOGIN_URL)
def drafts(request):
    """
    Description: Unpublished posts of current authenticated user.
    
    Arguments:   - request: HttpRequest object
    Return:      HttpResponse
                                  
    Author:      Nnoduka Eruchalu
    """
    posts_list = Post.objects.filter(is_public=False, user=request.user)
    return posts_helper(request, posts_list, None, "My Drafts")


@login_required
@permission_required('blog.add_post', login_url=settings.LOGIN_URL)
def create(request):
    """
    Description: Create a blog post
    
    Arguments:   - request: HttpRequest object
    Return:      HttpResponse
                                  
    Author:      Nnoduka Eruchalu
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user # who is uploading this?
            post.save()              # finally create db record
            form.save_m2m()          # this is to save tags
            messages.add_message(
                request, messages.SUCCESS, "Post successfully created")
            return HttpResponseRedirect(reverse("posts"))
            
    else:
        form = PostForm()
    
    return render_to_response("blog/create.html",
                              {'form':form},
                              context_instance = RequestContext(request))


@login_required
@permission_required('blog.change_post', login_url=settings.LOGIN_URL)
def edit(request, id):
    """
    Description: Edit a given blog post
    
    Arguments:   - request: HttpRequest object
                 - id: Id of Blog Post of interest
    Return:      HttpResponse
                                  
    Author:      Nnoduka Eruchalu
    """
    post = get_object_or_404(Post, id=id)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "Post successfully edited")
            return HttpResponseRedirect(reverse("postDetail",
                                                kwargs={'id':id})
                                        )
    
    # if request.method != 'POST'
    else:
        form = PostForm(instance=post)
    
    return render_to_response("blog/edit.html",
                              {'form':form},
                              context_instance = RequestContext(request))
        
@login_required
@require_http_methods(["POST"])
@permission_required('blog.delete_post', login_url=settings.LOGIN_URL)
def delete(request, id):
    """
    Description: Delete a given blog post
    
    Arguments:   - request: HttpRequest object
                 - id: Id of Blog Post of interest
    Return:      HttpResponse
                                  
    Author:      Nnoduka Eruchalu
    """
    post = get_object_or_404(Post, id=id)
    
    try:
        post.delete()
        messages.add_message(
            request, messages.SUCCESS, "Post successfully deleted")
    except Post.DoesNotExist:
        messages.add_message(
            request, messages.ERROR, "Post couldn't be deleted")
        
    return HttpResponseRedirect(reverse("posts"))


