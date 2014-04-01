from django.conf.urls import patterns, url

from ycp.apps.ckeditor import views

urlpatterns = patterns('',
                       # upload image
                       url(r'^upload/$', views.upload, name="ckeditorUpload"),
                       
                       # upload file
                       url(r'^upload/file$', views.uploadFile,
                           name="ckeditorUploadFile"),
                       
                       # browse images
                       url(r'^browse/$', views.browse, name="ckeditorBrowse"),
                       )
