from django.conf.urls import patterns, include, url

from ycp.apps.tag import views

urlpatterns = patterns('',
                                              
                       # get posts and media with a tag
                       url(r'^(?P<tag>[\w\W]+)/$', views.details,
                           name="tagDetails"),
                       )
