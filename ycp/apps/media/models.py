from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from datetime import datetime
from cStringIO import StringIO
import os, re, unicodedata, zipfile

from ycp.utils import get_upload_path
from ycp.apps.photo.models import Photo
from ycp.apps.youtube.models import Video

try:
    from PIL import Image
except ImportError:
    import Image


# ---------------------------------------------------------------------------- #
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------- #

def get_zip_path(instance, filename):
    """
    Description: Determine a unique temporary upload path for a given zip file.
    
    Arguments:   - instance: Gallery model instance which uses zip file to
                             extract photos
                 - filename: filename that was originally given to the file
    Return:      Unique filepath for given file, that's a subpath of `temp/`
            
    Author:      Nnoduka Eruchalu
    """
    return get_upload_path(instance, filename, 'temp/')



# ---------------------------------------------------------------------------- #
# MODEL CLASSES
# ---------------------------------------------------------------------------- #

class Gallery(models.Model):
    """
    Description: gallery of media files (yup photo or video)
    
    Author:      Nnoduka Eruchalu
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created = models.DateTimeField(default=datetime.now, editable=False)
    user = models.ForeignKey(User,editable=False,verbose_name="gallery creator")
    
    class Meta:
        ordering = ['-created']
        get_latest_by = 'created'
    
    def __unicode__(self):
        return self.title
    
    def media_count(self):
        """
        Description: Return count of media items in gallery
                
        Arguments:   None
        Return:      None 
          
        Author:      Nnoduka Eruchalu
        """
        return self.media_set.all().count()
    
    def cover_photo(self):
        """
        Description: Get cover photo of gallery, which is thumbnail image of
                     latest addition to gallery
                
        Arguments:   None
        Return:      None 
          
        Author:      Nnoduka Eruchalu
        """
        try:
            latest_media = self.media_set.latest('created')
            return latest_media.thumbnail()
        except Media.DoesNotExist:
            return None;
    
    def bigimage_url(self):
        """
        Description: Larger version of cover_photo (but actual url)
                
        Arguments:   None
        Return:      None 
          
        Author:      Nnoduka Eruchalu
        """
        try:
            latest_media = self.media_set.latest('created')
            return latest_media.bigimage_url()
        except Media.DoesNotExist:
            return None;
        
            
    def delete(self, *args, **kwargs):
        """
        Description: Delete gallery, but first delete all media items in it.
                                                 
        Arguments:   *args, **kwargs
        Return:      None 
          
        Author:      Nnoduka Eruchalu
        """
        for media in self.media_set.all():
            media.delete()
        return super(Gallery, self).delete(*args, **kwargs)
        


class GalleryUpload(models.Model):
    """
    Description: Tool for uploading to gallery
    
    Author:      Nnoduka Eruchalu
    """
    # zip file of media items to be uploaded
    zip_file = models.FileField(
        upload_to=get_zip_path,
        storage=FileSystemStorage(),
        help_text="select a .zip file of images to upload")
    
    # gallery to upload image to
    gallery = models.ForeignKey(
        Gallery, null=True, blank=True,
        help_text="pick a gallery to add images to. Leave empty to create new with title and description")
    
    # gallery title
    title = models.CharField(max_length=200, blank=True)
    # gallery description
    description = models.TextField(blank=True)
    # gallery creator
    user = models.ForeignKey(User,editable=False,verbose_name="gallery creator")
    
    
    def save(self, *args, **kwargs):
        """
        Description: Save gallery upload files but delete this helper object
                     when done.
                                                 
        Arguments:   *args, **kwargs
        Return:      None 
          
        Author:      Nnoduka Eruchalu
        """
        super(GalleryUpload, self).save(*args, **kwargs)
        gallery = self.process_zipfile()
        self.delete()
        return gallery
    

    def delete(self, *args, **kwargs):
        """
        Description: Delete galleryUpload data (including its temporary zip 
                     file) from storage
                                                 
        Arguments:   *args, **kwargs
        Return:      None 
          
        Author:      Nnoduka Eruchalu
        """
        self.zip_file.delete(save=False)
        return super(GalleryUpload, self).delete(*args, **kwargs)
    
        
    def process_zipfile(self):
        """
        Description: process uploaded zipfile, by extracting images in zip and
                     uploading them to gallery.
                                                 
        Arguments:   None
        Return:      None 
          
        Author:      Nnoduka Eruchalu
        """
        if os.path.isfile(self.zip_file.path):
            # TODO: implement try-except here
            zip = zipfile.ZipFile(self.zip_file.path)
            bad_file = zip.testzip()
            if bad_file:
                raise Exception(
                    '"%s" in the .zip archive is corrupt.' % bad_file)
            
            if self.gallery:
                gallery = self.gallery
            else:
                gallery = Gallery.objects.create(title=self.title,
                                                 description=self.description,
                                                 user=self.user)
            
            count = 1 # number of files
            for filename in sorted(zip.namelist()):
                if filename.startswith('__'): # do not process meta files
                    continue
                data = zip.read(filename)
                if len(data):
                    try:
                        # the following is taken from django ImageField
                        #   load() could spot a truncated JPEG, but it loads the
                        #   entire image in memory, which is a DoS vector.
                        #   verify() must be called immediately after the
                        #   constructor.
                        Image.open(StringIO(data)).verify()
                    except Exception: # PIL didn't recognize it as an image
                        # if a "bad" file is found we just skip it.
                        continue
                    
                    title = ' '.join([self.title, str(count)])
                    photo = Photo(title=title,user=self.user)
                    photo.photo.save(filename,ContentFile(data))
                    gallery.media_set.add(photo.media)
                    count = count + 1
            zip.close()
            return gallery
                    

    
class Media(models.Model):
    """
    Description: Media object, either photo or video.
    
    Notes:       This model doesn't do error checking so use it with caution!
                 Only save video or photo to each object! but not both
    
    Author:      Nnoduka Eruchalu
    """
    # media object's photo or video. Can't have both!
    video = models.OneToOneField(Video, null=True, blank=True, default=None,
                                 editable=False)
    photo = models.OneToOneField(Photo, null=True, blank=True, default=None,
                                 editable=False)
    # media object's associated gallery
    gallery = models.ForeignKey(Gallery, null=True, blank=True)
    # media objet creation date. 
    created = models.DateTimeField(default=datetime.now, editable=False)
    
    class Meta:
        ordering = ['-created']
        get_latest_by = 'created'
    
    def __unicode__(self):
        title = "no content"
        if self.video:
            title = "video: %s" % (self.video.title)
        elif self.photo:
            title = "photo: %s" % (self.photo.title)
        return title
    
    
    def delete(self, *args, **kwargs):
        """
        Description: Delete media object, but first delete associated video or 
                     photo object.
                                                 
        Arguments:   *args, **kwargs
        Return:      None 
          
        Author:      Nnoduka Eruchalu
        """
        if self.video:
            self.video.delete(*args, **kwargs)
        else:
            self.photo.delete(*args, **kwargs)
        return super(Media, self).delete(*args, **kwargs)
    
    def thumbnail(self):
        """
        Description: Video or photo thumbnail object
        
        Arguments:   None
        Return:      None
        
        Author:      Nnoduka Eruchalu
        """
        if self.video:
            return self.video.default_thumbnail()
        else:
            return self.photo.thumbnail
        
    def bigimage_url(self):
        """
        Description: Larger version of thumbnail (but actual url)
        
        Arguments:   None
        Return:      None
        
        Author:      Nnoduka Eruchalu
        """
        if self.video:
            return self.video.default_thumbnail().url
        else:
            return self.photo.get_absolute_url()
        
    def title(self):
        """
        Description: Video or photo title
        
        Arguments:   None
        Return:      None
        
        Author:      Nnoduka Eruchalu
        """
        if self.video:
            return self.video.title
        else:
            return self.photo.title
        
    def mid(self):
        """
        Description: `mid` is media id (video or photo id)
        
        Arguments:   None
        Return:      None
        
        Author:      Nnoduka Eruchalu
        """
        if self.video:
            return self.video.id
        else:
            return self.photo.id
        
    def tags(self):
        """
        Description: media object's tags (video or photo tags)
        
        Arguments:   None
        Return:      None
        
        Author:      Nnoduka Eruchalu
        """
        if self.video:
            return self.video.tags.all()
        else:
            return self.photo.tags.all()
        
    def description(self):
        """
        Descripiton: media object's description
        
        Arguments:   None
        Return:      None
        
        Author:      Nnoduka Eruchalu
        """
        if self.video:
            return self.video.description
        else:
            return self.photo.description
    
    def object(self):
        """
        Description: media object
        
        Arguments:   None
        Return:      None
        
        Author:      Nnoduka Eruchalu
        """
        return self.video or self.photo

