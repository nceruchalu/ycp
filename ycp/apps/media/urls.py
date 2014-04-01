from django.conf.urls import patterns, url

from ycp.apps.media import views

urlpatterns = patterns('',
                       # media library
                       url(r'^$', views.library,
                           name="mediaLibrary"),
                       
                       # media galleries
                       url(r'^gallery/$', views.gallery,
                           name="mediaGallery"),
                       
                        # zoom into a gallery
                       url(r'^gallery/(?P<id>\d+)/$', views.galleryContent,
                           name="mediaGalleryContent"),
                       
                       # get details of a media item
                       url(r'^(?P<id>\d+)/$', views.mediaDetail,
                           name="mediaDetail"),
                       
                       # get details of a photo
                       url(r'^detail/photo/(?P<id>\d+)/$',
                           views.detailPhoto,
                           name="mediaPhotoDetail"),
                       
                       # get details of a video
                       url(r'^detail/video/(?P<id>\d+)/$',
                           views.detailVideo,
                           name="mediaVideoDetail"),
                                              
                       # upload zip file of pictures
                       url(r'^gallery/upload/$', views.uploadZip,
                           name="mediaUploadZip"),
                       
                       # create gallery
                       url(r'^gallery/create/$', views.galleryCreate,
                           name="mediaGalleryCreate"),
                       
                       # edit gallery
                       url(r'^gallery/edit/(?P<id>\d+)/$', views.galleryEdit,
                           name="mediaGalleryEdit"),
                       
                       # delete gallery
                       url(r'^gallery/delete/(?P<id>\d+)/$',views.galleryDelete,
                           name="mediaGalleryDelete"),
                       )
