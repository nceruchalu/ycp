from django.contrib import admin
from django.forms import ModelForm
from ycp.apps.youtube.models import Video, Thumbnail



class VideoAdmin(admin.ModelAdmin):
    """
    Description: Representation of the Video model in the admin interface.
    
    Functions:   -has_add_permission: disable adding of Videos through admin
                                              
    Author:      Nnoduka Eruchalu
    """
    
    readonly_fields = ('user', 'video_id', 'youtube_url', 'swf_url', 'created',
                       'file_upload')
    exclude = ('video_file',)
    actions = None # bulk delete doesn't call object delete
    
    def has_add_permission(self, request): 
        """
        Description: Don't want users adding videos through admin... must use 
                     laid out views, or it won't work
                    
        Arguments:   - request: HttpRequest object representing current request
        Return:      Boolean: False
                    
        Author:      Nnoduka Eruchalu
        """
        return False

class ThumbnailAdmin(admin.ModelAdmin):
    """
    Description: Representation of the video Thumbnail model in the admin UI
    
    Functions:   -has_add_permission: disable adding of Thumbnails through admin
                                              
    Author:      Nnoduka Eruchalu
    """
    
    readonly_fields = ('video', 'url')
    
    def has_add_permission(self, request): 
        """
        Description: Don't want user's adding thumbnails. This should only be 
                     done by Video model's save()
        
        Arguments:   - request: HttpRequest object representing current request
        Return:      Boolean: False
                    
        Author:      Nnoduka Eruchalu
        """
        return False
    
admin.site.register(Video, VideoAdmin)
admin.site.register(Thumbnail, ThumbnailAdmin)

