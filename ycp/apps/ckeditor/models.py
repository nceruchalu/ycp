from django.db import models

from django.core.urlresolvers import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize, Adjust
from ycp.utils import get_upload_path
from django.contrib.auth.models import User

from datetime import datetime
import os, re, unicodedata

# Create your models here.

# ---------------------------------------------------------------------------- #
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------- #

def slugify(string):
    s = unicode(string)
    slug = unicodedata.normalize('NFKD', s)
    slug = slug.encode('ascii', 'ignore').lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    slug = re.sub(r'[-]+', '-', slug)
    return slug


def get_image_path(instance, filename):
    """
    Description: Determine a unique upload path for a given image file
    
    Arguments:   - instance: Album model instance where file is being attached
                 - filename: filename that was originally given to the file
    Return:      Unique filepath for given file, that's a subpath of `ckeditor/`
            
    Author:      Nnoduka Eruchalu
    """
    return get_upload_path(instance, filename, 'ckeditor/')

def get_file_path(instance, filename):
    """
    Description: Determine a unique upload path for a given non-image file
    
    Arguments:   - instance: Album model instance where file is being attached
                 - filename: filename that was originally given to the file
    Return:      Unique filepath for given file, that's a subpath of 
                 `ckeditor/file/`
            
    Author:      Nnoduka Eruchalu
    """
    return get_upload_path(instance, filename, 'ckeditor/file/')
    

# ---------------------------------------------------------------------------- #
# MODEL CLASSES
# ---------------------------------------------------------------------------- #

class Image(models.Model):
    """
    Description: Every Image object is attached to a rich text field edited
                 with CKEditor's WYSIWYG editor.
                                                      
    Author:      Nnoduka Eruchalu
    """
    
    # image
    image = models.ImageField(upload_to=get_image_path)
    # creation date
    created = models.DateTimeField(default=datetime.now, editable=False)
    # image uploader
    user = models.ForeignKey(User, editable=False,verbose_name="image uploader")
    
    # imagekit specs for image used for post thumbnail images
    ckthumbnail = ImageSpecField(
        source='image',
        processors=[SmartResize(width=75, height=75),
                    Adjust(contrast = 1.2, sharpness=1.1)],
        format='JPEG',
        options={'quality':90})
    
    # imagekit specs for image used in post
    ckpost = ImageSpecField(
        source='image',
        processors=[SmartResize(width=300, height=300),
                    Adjust(contrast = 1.2, sharpness=1.1)],
        format='JPEG',
        options={'quality':90})
    
    class Meta:
        ordering = ['-created']
        get_latest_by = 'created'
    
    def __unicode__(self):
        return "uploaded on: %s" % self.created
    
    
    def get_absolute_url(self):
        return self.image.url

    def delete_image_files(self, instance):
        """
        Description: Delete richtext embedded-image files in storage
                     - First delete the model's ImageCacheFiles on storage
                       The reason this must happen first is that deleting source
                       file deletes the associated ImageCacheFile references but
                       not the actual ImageCacheFiles in storage.
                     - Next delete source file (this also performs a delete on
                       the storage backend)
                
        Arguments:   - instance: Image object instance to have files deleted
        Return:      None 
          
        Author:      Nnoduka Eruchalu
        """
        # get thumbnail location and delete it
        instance.ckthumbnail.storage.delete(instance.ckthumbnail.name)
        # do same for post image
        instance.ckpost.storage.delete(instance.ckpost.name)
        # delete image
        instance.image.delete()
            
    def delete(self, *args, **kwargs):
        """
        Description: Default model delete doesn't delete files on storage,
                     so force that to happen.
                                                 
        Arguments:   *args, **kwargs
        Return:      None 
          
        Author:      Nnoduka Eruchalu
        """
        if self.image:
            self.delete_image_files(self)
        
        return super(Image, self).delete(*args, **kwargs)



class File(models.Model):
    """
    Description: Every Non-image File object is attached to a rich text field 
                 edited with CKEditor's WYSIWYG editor.
                                                      
    Author:      Nnoduka Eruchalu
    """
    # file
    file = models.FileField(upload_to=get_file_path)
    # creation datetime
    created = models.DateTimeField(default=datetime.now, editable=False)
    # file uploader
    user = models.ForeignKey(User, editable=False,verbose_name="file uploader")
    
    class Meta:
        ordering = ['-created']
        get_latest_by = 'created'
            
    def __unicode__(self):
        return "uploaded on: %s" % self.created
        
    def get_absolute_url(self):
        return self.file.url
    
    def delete(self, *args, **kwargs):
        """
        Description: Default model delete doesn't delete files on storage,
                     so force that to happen.
                                                 
        Arguments:   *args, **kwargs
        Return:      None 
          
        Author:      Nnoduka Eruchalu
        """
        self.file.delete(save=False)
        return super(File, self).delete(*args, **kwargs)
    

