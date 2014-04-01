from django.conf.urls import patterns, include, url

from ycp.apps.youtube import views

urlpatterns = patterns('',
                       # browser-based uploading
                       url(r'^upload/$', views.uploadBrowser,
                           name="youtubeUploadBrowser"),
                       
                       # YouTube's return location after browser-based upload
                       url(r'^upload/return/$', views.uploadBrowserReturn,
                           name="youtubeUploadBrowserReturn"),
                       
                       # direct uploading
                       url(r'^upload/direct/$', views.uploadDirect,
                           name="youtubeUploadDirect"),
                       
                       # upload by entering url
                       url(r'^upload/url/$', views.uploadUrl,
                           name="youtubeUploadUrl"),
                       
                       # edit
                       url(r'^edit/(?P<id>\d+)/$', views.edit,
                           name="youtubeEdit"),
                       
                       # delete
                       url(r'^delete/(?P<id>\d+)/$', views.delete,
                           name="youtubeDelete"),
                       )
