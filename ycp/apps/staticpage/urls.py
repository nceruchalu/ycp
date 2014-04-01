from django.conf.urls import patterns, include, url

from ycp.apps.staticpage import views

urlpatterns = patterns('',
                       # ---- ABOUT
                       # about
                       url(r'^about/$', views.direct_to_template,
                           {'template':'staticpage/about/about.html',
                            'kwargs':{'currentnav':'about'}
                           },
                           name="about"),
                       
                       # contact us 
                       url(r'^contact/$', views.contact,
                           name="contact"),
                       
                       # power quotes
                       url(r'^quotes/$', views.direct_to_template,
                           {'template':'staticpage/about/quotes.html',
                            'kwargs':{'currentnav':'quotes'}
                           },
                           name="quotes"),
                       
                       
                       # ----- GET INVOLVED
                       # get involved
                       url(r'^getinvolved/$', views.direct_to_template,
                           {'template':
                                'staticpage/getinvolved/getinvolved.html',
                            'kwargs':{'currentnav':'getinvolved'}
                           },
                           name="getinvolved"),
                       
                       # scholarships
                       url(r'^scholarships/$', views.direct_to_template,
                           {'template':
                                'staticpage/getinvolved/scholarships.html',
                            'kwargs':{'currentnav':'scholarships'}
                           },
                           name="scholarships"),
                       
                       # cfp challenge
                       url(r'^cfpchallenge/$', views.direct_to_template,
                           {'template':
                                'staticpage/getinvolved/cfpchallenge.html',
                            'kwargs':{'currentnav':'cfpchallenge'}
                           },
                           name="cfpchallenge"),
                       
                       # training programs
                       url(r'^trainingprograms/$', views.direct_to_template,
                           {'template':
                                'staticpage/getinvolved/trainingprograms.html',
                            'kwargs':{'currentnav':'trainingprograms'}
                           },
                           name="trainingprograms"),
                       
                       # consortium basket
                       url(r'^consortiumbasket/$', views.direct_to_template,
                           {'template':
                                'staticpage/getinvolved/consortiumbasket.html',
                            'kwargs':{'currentnav':'consortiumbasket'}
                           },
                           name="consortiumbasket"),
                       
                       # grassroot projects
                       url(r'^grassrootprojects/$', views.direct_to_template,
                           {'template':
                                'staticpage/getinvolved/grassrootprojects.html',
                            'kwargs':{'currentnav':'grassrootprojects'}
                           },
                           name="grassrootprojects"),
                       
                       
                       # ---- PROJECTS
                       # cheetah generation radio show
                       url(r'^cheetahradio/$', views.direct_to_template,
                           {'template':
                                'staticpage/projects/cheetahradio.html',
                            'kwargs':{'currentnav':'cheetahradio'}
                            },
                           name="cheetahradio"),
                       
                       # under the innovation influence campaign
                       url(r'^innovationinfluence/$', views.direct_to_template,
                           {'template':
                                'staticpage/projects/innovationinfluence.html',
                            'kwargs':{'currentnav':'innovationinfluence'}
                            },
                           name="innovationinfluence"),
                       
                       )
