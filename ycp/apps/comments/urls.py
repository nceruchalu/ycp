from django.conf.urls import patterns, include, url

from ycp.apps.comments import views

urlpatterns = patterns('',
                       
                       # post comments
                       url(r'^post/$', views.post_comment,
                           name="commentsPost"),
                       )
