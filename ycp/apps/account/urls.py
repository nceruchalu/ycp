from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from ycp.apps.account import views

urlpatterns = patterns('',
                       url(r'^login/$', views.custom_login,
                           {'template_name':'account/login.html'},
                           name="login"),
                       
                       url(r'^logout/$', auth_views.logout,
                        {'next_page':'/'}, name="logout"),
                       
                       url(r'^password/change/$',
                           auth_views.password_change,
                           {'template_name':'account/password_change.html'},
                           name='acct_password_change'),
                       
                       url(r'^password/change/done/$',
                           auth_views.password_change_done,
                           {'template_name':'account/password_change_done.html'},
                           name='password_change_done'),
                       
                       url(r'^password/reset/$',
                           auth_views.password_reset,
                           {'template_name':'account/password_reset.html',
                            'email_template_name':
                                'account/password_reset_email.txt',
                            'subject_template_name':
                                'account/password_reset_email_subject.txt',
                            'post_reset_redirect':
                                'acct_password_reset_done'},
                           name='acct_password_reset'),
                       
                       url(r'^password/reset/done/$',
                           auth_views.password_reset_done,
                           {'template_name':'account/password_reset_done.html'},
                           name='acct_password_reset_done'),
                       
                       url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           auth_views.password_reset_confirm,
                           {'template_name':'account/password_reset_confirm.html'},
                           name='acct_password_reset_confirm'),
                       
                       url(r'^password/reset/complete/$',
                           auth_views.password_reset_complete,
                           {'template_name':'account/password_reset_complete.html'},
                           name='password_reset_complete'),
                       
                       )
