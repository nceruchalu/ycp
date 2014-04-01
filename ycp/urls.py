from django.conf.urls import patterns, include, url
from ycp import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', views.homepage, name="homepage"),
                       url(r'^search/$', views.search, name="search"),
                       url(r'^opensearch.xml$', views.opensearch,
                           name="opensearch"),
                       url(r'^', include('ycp.apps.account.urls')),
                       url(r'^', include('ycp.apps.staticpage.urls')),
                       url(r'^video/', include('ycp.apps.youtube.urls')), 
                       url(r'^photo/', include('ycp.apps.photo.urls')),
                       url(r'^media/', include('ycp.apps.media.urls')),
                       url(r'^ckeditor/', include('ycp.apps.ckeditor.urls')),
                       url(r'^post/', include('ycp.apps.blog.urls')), 
                       url(r'^djangocomments/',
                           include('django.contrib.comments.urls')),
                       url(r'^comments/', include('ycp.apps.comments.urls')),
                       url(r'^tag/', include('ycp.apps.tag.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       
                       # Examples
                       # url(r'^$', 'ycp.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
)
