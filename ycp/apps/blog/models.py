from django.db import models
from ycp.apps.ckeditor.fields import RichTextField
from datetime import datetime
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.
class Post(models.Model):
    """
    Description: Representaton of Blog Post objects
                                                      
    Author:      Nnoduka Eruchalu
    """
    
    # post title
    title = models.CharField(max_length=200)
    
    # content, to be edited in a WYSIWYG HTML text editor
    content = RichTextField()
    
    # tags
    tags = TaggableManager(blank=True)
    
    # post has been published?
    is_public = models.BooleanField(
        verbose_name='publish', default=False,
        help_text="can't unpublish after you publish")
    
    # creation date
    created = models.DateTimeField(default=datetime.now, editable=False)
    # creator
    user = models.ForeignKey(User, editable=False,verbose_name="post creator")
    
    class Meta:
        ordering = ['-created']
        get_latest_by = 'created'
    
    def __unicode__(self):
        return self.title
    
    
    def get_cname(self):
        """
        Description: return class name for use in templates
        
        Arguments:   None
        Return:      string representation of Post object's class name.
        
        Author:      Nnoduka Eruchalu
        """
        return "post"
    
    
    def save(self, *args, **kwargs):
        """
        Description: On a Post save, if it has been published, never allow it be
                     unpublished. If this is first time post is being published
                     update the creation date.
        
        Arguments:   *args, **kwargs
        Return:      None 
          
        Author:      Nnoduka Eruchalu
        """
        if self._get_pk_val() is not None:
            orig = Post.objects.get(pk = self._get_pk_val())
            
            if orig.is_public == True:
                # no going back if already published
                self.is_public = True
                            
            if (orig.is_public != self.is_public) and (orig.is_public==False):
                # publish status changed to True so update 'created'
                self.created = datetime.now()
                                    
        super(Post, self).save(*args, **kwargs)

        
    def delete(self, *args, **kwargs):
        """
        Description: On a Post delete, clear all its tags from tags-manager.
        
        Arguments:   *args, **kwargs
        Return:      None 
          
        Author:      Nnoduka Eruchalu
        """
        # clear tags()
        self.tags.clear()
                
        # call the super method
        return super(Post, self).delete(*args, **kwargs)

