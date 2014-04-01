from django.contrib import admin
from ycp.apps.media.models import Media, Gallery, GalleryUpload


class GalleryAdmin(admin.ModelAdmin):
    """
    Description: Representation of the Gallery model in the admin interface.
    
    Functions:   -has_add_permission: disable adding of Galleries through admin
                                              
    Author:      Nnoduka Eruchalu
    """
    
    readonly_fields = ('created','user')
    actions = None # bulk delete doesn't call object delete
    
    def has_add_permission(self, request): 
        """
        Description: Don't want user's adding Galleries through admin 
          
        Arguments:   - request: HttpRequest object representing current request
        Return:      Boolean: False
                    
        Author:      Nnoduka Eruchalu
        """
        return False


class MediaAdmin(admin.ModelAdmin):
    """
    Description: Representation of the Media model in the admin interface.
    
    Functions:   -has_add_permission: disable adding of Media through admin
                                              
    Author:      Nnoduka Eruchalu
    """
    
    readonly_fields = ('video', 'photo', 'created')
    actions = None # bulk delete doesn't call object delete
    
    def has_add_permission(self, request): 
        """
        Description: Don't want user's adding Media through admin 
          
        Arguments:   - request: HttpRequest object representing current request
        Return:      Boolean: False
                    
        Author:      Nnoduka Eruchalu
        """
        return False

admin.site.register(Media, MediaAdmin)
admin.site.register(Gallery, GalleryAdmin)


