from django.conf.urls import patterns, include, url

from ycp.apps.photo import views

urlpatterns = patterns('',
                       # photo uploading
                       url(r'^upload/$', views.upload,
                           name="photoUpload"),
                       
                       # photo uploading with url
                       url(r'^upload/url$', views.uploadUrl,
                           name="photoUploadUrl"),
                                              
                       # edit
                       url(r'^edit/(?P<id>\d+)/$', views.edit,
                           name="photoEdit"),
                       
                       # delete
                       url(r'^delete/(?P<id>\d+)/$', views.delete,
                           name="photoDelete"),
                       )
