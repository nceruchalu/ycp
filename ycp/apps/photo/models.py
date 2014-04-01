from django.db import models
from datetime import datetime
import os, re, unicodedata

from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize, Adjust
from ycp.utils import get_upload_path

from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.

# ---------------------------------------------------------------------------- #
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------- #

def get_image_path(instance, filename):
    """
    Description: Determine a unique upload path for a given photo image file
    
    Arguments:   - instance: Photo model instance where file is being attached
                 - filename: filename that was originally given to the file
    Return:      Unique filepath for given file, that's a subpath of `photo/`
            
    Author:      Nnoduka Eruchalu
    """
    return get_upload_path(instance, filename, 'photo/')


# ---------------------------------------------------------------------------- #
# MODEL CLASSES
# ---------------------------------------------------------------------------- #

class Photo(models.Model):
    """
    Description: These are the photos uploaded to the general library or 
                 galleries
                                                      
    Author:      Nnoduka Eruchalu
    """
    
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to=get_image_path)
    # phtoo tags
    tags = TaggableManager(blank=True)
    # photo creation time
    created = models.DateTimeField(default=datetime.now, editable=False)
    # photo uploader
    user = models.ForeignKey(User, editable=False,verbose_name="photo uploader")
    
    # imagekit spec for gallery thumbnail images
    thumbnail = ImageSpecField(
        source='photo',
        processors=[SmartResize(width=218, height=150),
                    Adjust(contrast = 1.2, sharpness=1.1)],
        format='JPEG',
        options={'quality':90})

    # imagekit spec for search result page thumbnail images
    smallthumbnail = ImageSpecField(
        source='photo',
        processors=[SmartResize(width=90, height=62),
                    Adjust(contrast = 1.2, sharpness=1.1)],
        format='JPEG',
        options={'quality':90})
    
    # imagekit spec for homepage slider images
    slider = ImageSpecField(
        source='photo',
        processors=[SmartResize(width=379, height=200),
                    Adjust(contrast = 1.2, sharpness=1.1)],
        format='JPEG',
        options={'quality':90})
    
    
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
        return "photo"
        
    def get_absolute_url(self):
        return self.photo.url
    
    
    def save(self, *args, **kwargs):
        """
        Description: When saving a Photo object, if it's a new instance create
                     associated media object.
        
        Arguments:   *args, **kwargs
        Return:      None
        
        Author:      Nnoduka Eruchalu
        """
        # if this is a new instance
        if self._get_pk_val() is None:
            super(Photo, self).save(*args, **kwargs)
            
            # can't import on startup... because Media imports this file
            from ycp.apps.media.models import Media
            Media(photo=self).save()
        
        # if this is an instance being updated
        else:
            super(Photo, self).save(*args, **kwargs)
    
    def delete_photo_files(self, instance):
        """
        Description: Delete a photo's image files in storage
                     - First delete the model's ImageCacheFiles on storage
                       The reason this must happen first is that deleting source
                       file deletes the associated ImageCacheFile references but
                       not the actual ImageCacheFiles in storage.
                     - Next delete source file (this also performs a delete on
                       the storage backend)
                
        Arguments:   - instance: Photo object instance to have files deleted
        Return:      None 
          
        Author:      Nnoduka Eruchalu
        """
        # get thumbnail location and delete it
        instance.thumbnail.storage.delete(instance.thumbnail.name)
        # do same for smallthumbnail
        instance.smallthumbnail.storage.delete(instance.smallthumbnail.name)
        # and also for homepage slider
        instance.slider.storage.delete(instance.slider.name)
        # delete photo
        instance.photo.delete()

    def delete(self, *args, **kwargs):
        """
        Description: model delete doesn't delete files on storage, so force that
                     to happen. Then delete associate tags.
                     
        Arguments:   *args, **kwargs
        Return:      None
        
        Author:      Nnoduka Eruchalu
        """
        if self.photo:
            self.delete_photo_files(self)
            
        # delete tags
        self.tags.clear()
        
        return super(Photo, self).delete(*args, **kwargs)
