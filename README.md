# Youth Consortium for Progress (YCP)

## About YCP
|         |                                             |
| ------- | ------------------------------------------- |
| Author  | Nnoduka Eruchalu                            |
| Date    | 03/14/2014                                  |
| Website | [http://ycp.nceruchalu.webfactional.com/][ycp-site] |

[YCP][ycp-site] is a network of young people across the globe committed to progress through hardwork, honesty and initiative and to sharing progressive ideas.

This site provides visitors with

* Views of photos, videos, and blog posts
* Optionally anonymous commenting on posted items.

Administrative users get added functionality of:

* Photo uploads: single photo, zipped photo archives
* Photo gallery manamagement
* Video uploads [hosted on YouTube]
* Blog Post management [using [CKEditor](http://ckeditor.com/)]

[ycp-site]:http://ycp.nceruchalu.webfactional.com


## Technologies
* Python
* MySQL
* Javascript
* HTML
* CSS
* Amazon Web Services


## Software Description
| Module              | Description                                            |
| ------------------- | ------------------------------------------------------ |
| `context_processors.py` | Context processor for passing site around          |
| `settings.py`       | Django settings for project                            |
| `urls.py`           | URL dispatcher for project                             |
| `utils.py`          | Utility functions useful to multiple Django apps       |
| `wsgi.py`           | WSGI config for YCP project                            |
|                     |                                                        |
| **`apps/`**         | Django apps with backend logic                         |
| `apps/account/`     | User account authentication app                        |
| `apps/blog/`        | Blog posts app                                         |
| `apps/ckeditor/`    | App for CKEditor integration with django project       |
| `apps/comments/`    | App for extension of `django.contrib.comments`         |
| `apps/media/`       | Media (Photos and Videos) representation app           |
| `apps/photo/`       | Photos and photo galleries app                         |
| `apps/staticpage/`  | Static site pages app                                  |
| `apps/tag/`         | App for extension of `django-taggit`                   |
| `apps/youtube/`     | Video management (via YouTube) app.                    |
|                     |                                                        |
| **`static/`**       | static files for project                               |
| `static/css/`       | CSS files                                              |
| `static/ckeditor/`  | CKEditor plugin files                                  |
| `static/galleriffic/` | Galleriffic plugin files                             |
| `static/img`        | Static images                                          |
| `static/js/`        | Javascript files                                       |
| `static/mobile/`    | Mobile Static files using Sencha Touch (JS, CSS, HTML) |
|                     |                                                        |
| **`templates/`**          | Django templates used by apps                    |
| `templates/404.html`      | 404 page                                         |
| `templates/500.html`      | 500 page                                         |
| `templates/headfoot.html` | base template used by all templates              |
| `templates/account/`      | templates used by `account` app's views          |
| `templates/blog/`         | templates used by `blog` app's views             |
| `templates/ckeditor/`     | templates used by `ckeditor` app's views         |
| `templates/comments/`     | templates used by `comments` app's views         |
| `templates/home/`         | template used for homepage                       |
| `templates/media/`        | templates used by `media` app's views            |
| `templates/photo/`        | templates used by `photo` app's views            |
| `templates/search/`       | templates and indexes  used by search view       |
| `templates/staticpage/`   | static page templates                            |
| `templates/tag/`          | templates used by `tag` app's views              |
| `templates/youtube/`      | templates used by `youtube` app's views          |


#### 3rd-party Python Modules
* [django](https://www.djangoproject.com/)
* [whoosh](https://bitbucket.org/mchaput/whoosh/wiki/Home)

###### The following modules have been saved in a local folder on PYTHONPATH
* [django imagekit](https://github.com/matthewwithanm/django-imagekit)
    * depends on [pilkit](https://github.com/matthewwithanm/pilkit)
    * depends on [django-appconf](https://github.com/jezdez/django-appconf)
        * depends on [six](https://pypi.python.org/pypi/six)
* [django storages](https://bitbucket.org/david/django-storages/overview)
    * specifically S3.py which
        * depends on [python-boto](https://github.com/boto/boto)
* [django haystack](https://github.com/toastdriven/django-haystack)
* [taggit](https://github.com/alex/django-taggit)
* [Google Data APIs Python Client Library, gdata](https://code.google.com/p/gdata-python-client/) 


#### 3rd-party Javascript Modules
* [jQuery](http://jquery.com/) 
* [Apprise-v2](http://labs.bigroomstudios.com/libraries/Apprise-v2)
* [Nivo Slider](http://dev7studios.com/plugins/nivo-slider)
* [CKEditor](http://ckeditor.com/)
* [Galleriffic](https://code.google.com/p/galleriffic/)


## Deployment:


### Settings files
The Django project is missing the `ycp/settings_secret.py` file. A template version is included for help in setting up the sensitive information needed by the project.


### Static Files Deployment

##### Generating Compressed JS & CSS Files
JS files in `noddymix/static/js/` and CSS files in `noddymix/static/css/` will be compressed to minimize browser download sizes.
All files will be gzipped using the command:
```
gzip -c <filename> > compressed/<filename>
```

##### Uploading static files
The static images, plugin modules (galleriffic and ckeditor) and  compressed css & js are uploaded to the appropriate AWS S3 bucket. Django's settings know to pick up files from there when not in DEBUG mode.


### Server Setup Notes
These instructions here are what I did on my [Webfaction](https://www.webfaction.com/) server.

#### `settings.py` Configurations:
`settings.py` expects to import a file called `settings_secret.py` in the `ycp/` folder. 
See `settings_secret.template.py` for what is required in the file.


#### Crontab Additions
Access crontab with:
```
crontab -e
```

Edit it to perform following functionality:

* Setup PATH, PYTHONPATH, NODE_PATH to be used by cron's environment
* Restart apache every 20 minutes. This ensures minimal downtime (if at all)
* Run management command to update search indexes every 12 hours.

```
PATH=/home/nceruchalu/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:.
PYTHONPATH=/home/nceruchalu/lib/python2.7:/home/nceruchalu/pythonlibs:/home/nceruchalu/webapps/ycp:/home/nceruchalu/webapps/ycp/ycp

6,26,46 * * * * ~/webapps/ycp/apache2/bin/start
0 */12 * * * /usr/local/bin/python2.7 ~/webapps/ycp/ycp/manage.py update_index > ~/cron/ycp_update_index.log 2>&1
```

## References:
Some apps based off the following sources:

* [django-ckeditor](https://github.com/shaunsephton/django-ckeditor)
* [django-youtube](https://github.com/laplacesdemon/django-youtube)


## Miscellaneous:

#### To Run Development Server
```
python manage.py runserver 0:8000
```

