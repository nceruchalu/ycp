from django.conf.urls import patterns, include, url

from ycp.apps.blog import views

urlpatterns = patterns('',
                       
                       # blog posts
                       url(r'^$', views.posts,
                           name="posts"),
                       
                       # get details of a post
                       url(r'^(?P<id>\d+)/$', views.postDetail,
                           name="postDetail"),
                       
                       # blog archives
                       url(r'^archives/$', views.archives,
                           name="postArchives"),
                       
                       # blog archives for a year
                       url(r'^archives/(?P<year>\d+)/$', views.archivesYear,
                           name="postArchivesYear"),
                       
                       # blog archives for a month
                       url(r'^archives/(?P<year>\d+)/(?P<month>\d+)/$', 
                           views.archivesMonth,
                           name="postArchivesMonth"),
                       
                       # blog post drafts
                       url(r'^drafts/$', views.drafts,
                           name="postDrafts"),
                       
                       # blog post creating
                       url(r'^create/$', views.create,
                           name="postCreate"),
                                              
                       # edit
                       url(r'^edit/(?P<id>\d+)/$', views.edit,
                           name="postEdit"),
                       
                       # delete
                       url(r'^delete/(?P<id>\d+)/$', views.delete,
                           name="postDelete"),
                       )
