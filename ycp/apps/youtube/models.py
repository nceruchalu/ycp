from django.db import models
from ycp.apps.youtube.api import Api
from datetime import datetime
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.
class Video(models.Model):
    """
    Description: These are the photos uploaded to the general library or 
                 galleries
                                                      
    Author:      Nnoduka Eruchalu
    """
    
    # YouTube insists on a title
    title = models.CharField(max_length=200) 
    
    # YouTube insists on a descriptions
    description = models.TextField()   
    
    # video tags
    tags = TaggableManager(
        help_text="comma separated and each at least 2 characters long",
        blank=True)
    
    # make video private on Youtube
    private = models.BooleanField(default=False)
    
    # video file to be uploaded
    video_file = models.FileField(
        upload_to='videos',
        storage='django.core.files.storage.FileSystemStorage',
        blank=True)
    
    # video uploader
    user = models.ForeignKey(User, editable=False,verbose_name="video uploader")
    # youtube video ID
    video_id = models.CharField(max_length=255, unique=True, editable=False)
    # youtube video watch page
    youtube_url = models.URLField(max_length=200, blank=True, editable=False)
    # youtube flash player URL
    swf_url = models.URLField(max_length=200, blank=True, editable=False)
    
    # video creation datetime
    created = models.DateTimeField(default=datetime.now, editable=False)
    
    # boolean indicating if video came from a file upload or a URL download
    file_upload = models.BooleanField(default=True, editable=False,
                                      verbose_name="video from file upload?")
    
    class Meta:
        ordering = ['-created']
        get_latest_by = 'created'
    
    def __unicode__(self):
        return self.title
    
    
    def get_cname(self):
        """
        Description: Get class name for use in templates
        
        Arguments:   None
        Return:      string of class name
        
        Author:      Nnoduka Eruchalu
        """
        return "video"
    
    
    def get_absolute_url(self):
        """
        Description: Get the swf url
        
        Arguments:   None
        Return:      string swf url
        
        Author:      Nnoduka Eruchalu
        """
        return self.swf_url
    
    def entry(self):
        """
        Description: Connect to Youtube Api and retrieves the video entry object
        
        Arguments:   None
        Return:      YouTube API video entry object
        
        Author:      Nnoduka Eruchalu
        """
        api = Api()
        api.authenticate()
        return api.getVideo(self.video_id)

    
    def sync_db(self, entry):
        """
        Description: Sync the db with the data from youtube
        
        Arguments:   -entry: YouTube API video entry object
        Return:      None
        
        Author:      Nnoduka Eruchalu
        """ 
        # set the details
        if self.file_upload:
            # if a file upload, the sync is simple
            self.title = entry.media.title.text
            self.description = entry.media.description.text
            self.tags.set(
                *[x.strip() for x in entry.media.keywords.text.split(',')])
        else:
            # if a url upload, only use YouTube video to fill in the blanks
            self.title = self.title or entry.media.title.text
            self.description = self.description or entry.media.description.text
            if (not self.tags.all()) and entry.media.keywords.text:
                self.tags.set(
                    *[x.strip() for x in entry.media.keywords.text.split(',')])
                
        self.youtube_url = entry.media.player.url
        self.swf_url = entry.GetSwfUrl()
        
        if entry.media.private:
            self.private = True
        else:
            self.private = False
    
    
    def save(self, *args, **kwargs):
        """
        Description: Synchronize the video info on db with that on YouTube
        
        Arguments:   *args, **kwargs
        Return:      None
        
        Author:      Nnoduka Eruchalu
        """
        # if this is a new instance add details from api
        if self._get_pk_val() is None:
            # save the instance so can call tags.set()
            super(Video, self).save(*args, **kwargs)
            
            # connect to api and get the details
            entry = self.entry()
            self.sync_db(entry)
                
            # save the instance
            super(Video, self).save(*args, **kwargs)
                
            # save thumbnails
            for thumbnail in entry.media.thumbnail:
                t = Thumbnail()
                t.url = thumbnail.url
                t.video = self
                t.save()
             
            # can't import on startup... because Media imports this file
            from ycp.apps.media.models import Media
            Media(video=self).save()
        
        # if this is an instance being updated
        else:
            if self.file_upload: # can only modify video if you own it
                # connect to the api and update the video on YouTube
                api = Api()
                api.authenticate()
                # Update the info on youtube
                keywords = [t.name for t in self.tags.all()]
                
                updated_entry = api.updateVideo(self.video_id, self.title,
                                                self.description, keywords,
                                                self.private)
                
                # and sync youtube and the db
                self.sync_db(updated_entry)
                
            # save the instance
            super(Video, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """
        Description: Deletes the video from youtube if you own the video
        
        Arguments:   *args, **kwargs
        Return:      None
        
        Author:      Nnoduka Eruchalu
        """
        if self.file_upload:
            api = Api()
            
            # authentication required for delete
            api.authenticate()
            
            # send YouTube delete request
            api.deleteVideo(self.video_id)

        # clear tags()
        self.tags.clear()
                
        # call the super method
        return super(Video, self).delete(*args, **kwargs)
    
    
    def default_thumbnail(self):
        """
        Description: Get the first thumbnail in thumbnails -- it is the largest
        
        Arguments:   None
        Return:      Thumbnail object
        
        Author:      Nnoduka
        """
        return self.thumbnail_set.all()[0]
    
    
    def small_thumbnail(self):
        """
        Description: return a small thumbnail, so second to 4th will work
        
        Arguments:   None
        Return:      Thumbnail object
        
        Author:      Nnoduka
        """
        return self.thumbnail_set.all()[1]
    


class Thumbnail(models.Model):
    """
    Description: These are the thumbnails associated with the YouTube-hosted
                 videos.
                                                      
    Author:      Nnoduka Eruchalu
    """
    
    # video that owns thumbnail
    video = models.ForeignKey(Video, null=True)
    # thumbnail URL
    url = models.URLField(max_length=200)
    
    def __unicode__(self):
        return "video: %s -+- thumbnail: %s" % (self.video.title, self.url)
    
    def get_absolute_url(self):
        return self.url
            

