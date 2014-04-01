from django.contrib import admin
from ycp.apps.photo.models import Photo

class PhotoAdmin(admin.ModelAdmin):
    """
    Description: Representation of the Photo model in the admin interface.
    
    Functions:   -has_add_permission: disable adding of Posts through admin
                                              
    Author:      Nnoduka Eruchalu
    """
    
    readonly_fields= ('photo', 'created', 'user')
    actions = None # bulk delete doesn't call object delete
    
    def has_add_permission(self, request): 
        """
        Description: Don't want users adding photos through admin... 
                     just wont work
          
        Arguments:   - request: HttpRequest object representing current request
        Return:      Boolean: False
                    
        Author:      Nnoduka Eruchalu
        """
        return False

admin.site.register(Photo, PhotoAdmin)

