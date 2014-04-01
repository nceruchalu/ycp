from django.contrib import admin
from ycp.apps.blog.models import Post

class PostAdmin(admin.ModelAdmin):
    """
    Description: Representation of the Post model in the admin interface.
    
    Functions:   -has_add_permission: disable adding of Posts through admin
                                              
    Author:      Nnoduka Eruchalu
    """
    
    readonly_fields = ('created','user',)
    
    def has_add_permission(self, request): 
        """
        Description: Don't want users adding blog posts through admin... 
                     just wont work
          
        Arguments:   - request: HttpRequest object representing current request
        Return:      Boolean: False
                    
        Author:      Nnoduka Eruchalu
        """
        return False

admin.site.register(Post, PostAdmin)
