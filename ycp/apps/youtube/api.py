"""
Description: gdata YouTube api interface

Reference:   https://github.com/laplacesdemon/django-youtube

Author:      Nnoduka Eruchalu
"""

import gdata
import gdata.youtube
import gdata.youtube.service
from django.conf import settings
import re

class BaseException(Exception):
    def __init__(self,value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)


class OperationError(BaseException):
    """
    Raise when an error happens on Api class
    """
    pass

class ApiError(BaseException):
    """
    Raise when a YouTube API related error occurs
    i.e. redirect Youtube errors with this error
    """
    pass


class Api(object):
    """
    Wrapper for Youtube API
    See docs @ https://developers.google.com/youtube/1.0/developers_guide_python
    """
    def __init__(self):
        self.yt_service = gdata.youtube.service.YouTubeService()
        
        try:
            self.yt_service.developer_key = settings.YOUTUBE_DEVELOPER_KEY
        except AttributeError:
            raise OperationError("Youtube Developer Key is missing in settings")
        
        try:
            self.yt_service.client_id = settings.YOUTUBE_CLIENT_ID
        except AttributeError:
            raise OperationError("Youtube Client ID is missing in settings")
            
        # Turn on HTTPS/SSL access.
        # Note: SSL is not available at this time for uploads.
        self.yt_service.ssl = False
        
        
    def authenticate(self):
        """
        This is ClientLogin authentication for installed applications
        """
        from gdata.service import BadAuthentication
        
        self.yt_service.email = settings.YOUTUBE_AUTH_EMAIL
        self.yt_service.password = settings.YOUTUBE_AUTH_PASSWORD
        self.yt_service.source = settings.YOUTUBE_CLIENT_ID
        try:
            self.yt_service.ProgrammaticLogin()
        except BadAuthentication:
            raise ApiError("Incorrect username or password")
        
    
    def getVideoFeed(self, uri):
        """
        get video entries in a video feed at a uri
        """
        return self.yt_service.GetYouTubeVideoFeed(uri)
    
    
    def getVideo(self, video_id):
        """
        retrieve a specific video entry
        """
        return self.yt_service.GetYouTubeVideoEntry(video_id=video_id)
        
    
    def printEntryDetails(self, entry):
        """
        print video entry contents
        """
        print 'Video title: %s' % entry.media.title.text
        print 'Video published on: %s ' % entry.published.text
        print 'Video description: %s' % entry.media.description.text
        print 'Video category: %s' % entry.media.category[0].text
        print 'Video tags: %s' % entry.media.keywords.text
        print 'Video watch page: %s' % entry.media.player.url
        print 'Video flash player URL: %s' % entry.GetSwfUrl()
        print 'Video duration: %s' % entry.media.duration.seconds
        
        # non entry.media attributes
        print 'Video geo location: %s' % repr(entry.geo.location())
        print 'Video view count: %s' % entry.statistics.view_count
        print 'Video rating: %s' % entry.rating.average
        
        # show alternate formats
        for alternate_format in entry.media.content:
            if 'isDefault' not in alternate_format.extension_attributes:
                print 'Alternate format: %s | url: %s ' % (
                    alternate_format.type,
                    alternate_format.url)
                
        # show thumbnails
        for thumbnail in entry.media.thumbnail:
            print 'Thumbnail url: %s' % thumbnail.url
    
            
    def printVideoFeed(self, feed):
        """
        print video feed entries
        """
        entry_number = 0
        for entry in feed.entry:
            entry_number += 1
            print "entry #%d" % entry_number
            self.printEntryDetails(entry)
    
    
    def getVideoFeedByUsername(self, username):
        """
        retrieving videos uploaded by a specific user
        """
        uri = 'http://gdata.youtube.com/feeds/api/users/%s/uploads' % username
        self.getVideoFeed(uri)
     
        
    def extractKeywords(self, keywords):
        """
        keywords is a list of keyword strings
        """
        kwds = ", ".join(keywords)#", ".join(re.findall(r"[\w']+", keywords))
        if not kwds: # blank string
            kwds = settings.YOUTUBE_UPLOAD_KEYWORDS
        return kwds
        
    def uploadDirect(self, title, description="",
                     keywords="",
                     category = settings.YOUTUBE_UPLOAD_CATEGORY,
                     private=False):
        """
        direct upload
        
        title = string, example "my test movie"
        description = string, example: "my description"
        keywords = string, example : "cars, funny"
        category = dictionary, example:{'term':'Nonprofit',
                                        'label':'Nonprofits & activisim'}
        private:True or False
        
        Returns:
        gdata.youtube.YouTubeVideoEntry
        """
        # setup keywords
        kwds = self.extractKeywords(keywords)
        # prepare a media group object to hold our video's meta-data
        my_media_group = gdata.media.Group(
            title=gdata.media.Title(text=title),
            description=gdata.media.Description(description_type='plain',
                                                text=description),
            keywords=gdata.media.Keywords(text=kwds),
            category=[gdata.media.Category(
                    text=category['term'],
                    scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
                    label=category['label'])],
            player=None,
            private = gdata.media.Private() if private else None
            )
            
        # prepare a geo.where object to hold the geographical location
        # of where the video was recorded
        #where = gdata.geo.Where()
        #where.set_location((37.0,-122.0))
        
        # create the gdata.youtube.YouTubeVideoEntry to be uploaded
        #video_entry = gdata.youtube.YouTubeVideoEntry(media=my_media_group,geo=where)
        video_entry = gdata.youtube.YouTubeVideoEntry(media=my_media_group)
        
        
        # set the path for the video file binary
        video_file_location = '/path/to/my/file.mov'
        
        new_entry = self.yt_service.InsertVideoEntry(video_entry,
                                                     video_file_location)
        return new_entry
        
    
    def uploadBrowser(self, title, description="",
                      keywords="",
                      category = settings.YOUTUBE_UPLOAD_CATEGORY,
                      private=False):
        """
        browser-based upload
        
        Simply Create a YouTubeVideoEntry that contains meta-data only. This
        video entry then gets posted to a special link on the YouTube API
        server. The XML response contains a token and a url which can then be
        used to upload the binary file using a standard HTML form.
        
        Returns:
            dictionary {'post_url':value, 'youtube_token':value}
        """
        kwds = self.extractKeywords(keywords)
                    
        # create media group as usual
        my_media_group = gdata.media.Group(
            title=gdata.media.Title(text=title),
            description=gdata.media.Description(description_type='plain',
                                                text=description),
            keywords=gdata.media.Keywords(text=kwds),
            category=[gdata.media.Category(
                    text=category['term'],
                    scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
                    label=category['label'])],
            player=None,
            private = gdata.media.Private() if private else None
            )
        
        # prepare a geo.where object to hold the geographical location
        # of where the video was recorded
        #where = gdata.geo.Where()
        #where.set_location((37.0,-122.0))
        
        # create the gdata.youtube.YouTubeVideoEntry to be uploaded
        #video_entry = gdata.youtube.YouTubeVideoEntry(media=my_media_group, geo=where)
        
        # create video entry as usual
        video_entry = gdata.youtube.YouTubeVideoEntry(media=my_media_group)
        
        # upload meta data only
        response = self.yt_service.GetFormUploadToken(video_entry)

        # parse response tuple and use the variables to build a form
        post_url = response[0]
        youtube_token = response[1]
        return {'post_url':post_url, 'youtube_token':youtube_token}


    def checkUploadStatus(self, video_id):
        """
        Checks the video upload status
        """
        entry = self.getVideo(video_id)
        upload_status = self.yt_service.CheckUploadStatus(entry)
        result = None
        if upload_status is not None:
            video_upload_state = upload_status[0]
            detailed_message = upload_status[1]
            result = {"upload_state":video_upload_state, 
                      "detaled_message":detailed_message}
        return result

    
    def updateVideo(self,video_id, title="", description="", keywords="",
                    private=None):
        """
        updating video information
        
        only pass in the parameters that have to be changed
        
        See: https://developers.google.com/youtube/2.0/developers_guide_protocol#Updating_and_deleting_videos
        
        Returns:
            updated entry
        """
        entry = self.getVideo(video_id)
        
        if title:
            entry.media.title.text = title
        
        if description:
            entry.media.description.text = description
            
        if keywords:
            kwds = self.extractKeywords(keywords)
            entry.media.keywords.text = kwds
        
        if (private==True or private==False):
            entry.media.private = gdata.media.Private() if private else None
        edit_uri = 'https://gdata.youtube.com/feeds/api/users/default/uploads/%s' % video_id
        updated_entry = self.yt_service.Put(entry, uri=edit_uri, 
        	converter=gdata.youtube.YouTubeVideoEntryFromString)
        return updated_entry
            

    def deleteVideo(self, video_id):
        """
        delete a video
        
        Returns:
            success status
        """
        edit_uri = 'https://gdata.youtube.com/feeds/api/users/default/uploads/%s' % video_id
        success = self.yt_service.Delete(edit_uri)
        return success
