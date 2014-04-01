from django.contrib import admin
from ycp.apps.ckeditor.models import Image, File


class ImageAdmin(admin.ModelAdmin):
    """
    Description: Representation of the CKEditor's Image model in the admin UI
    
    Functions:   -has_add_permission: disable adding of Images through admin
                                              
    Author:      Nnoduka Eruchalu
    """
    
    readonly_fields = ('image', 'created','user')
    actions = None # bulk delete doesn't call object delete
    
    def has_add_permission(self, request): 
        """
        Description: Don't want users adding Images through admin... 
                     Want all images to come directly from CKEditor's WYSIWYG
                     editor.
          
        Arguments:   - request: HttpRequest object representing current request
        Return:      Boolean: False
                    
        Author:      Nnoduka Eruchalu
        """
        return False

class FileAdmin(admin.ModelAdmin):
    """
    Description: Representation of the CKEditor's File model in the admin UI
    
    Functions:   -has_add_permission: disable adding of Files through admin
    
    Author:      Nnoduka Eruchalu
    """
     
    readonly_fields = ('file', 'created','user')
    actions = None # bulk delete doesn't call object delete
    
    def has_add_permission(self, request): 
        """
        Description: Don't want users adding Files through admin... 
                     Want all files to come directly from CKEditor's WYSIWYG
                     editor.
          
        Arguments:   - request: HttpRequest object representing current request
        Return:      Boolean: False
                    
        Author:      Nnoduka Eruchalu
        """
        return False

admin.site.register(Image, ImageAdmin)
admin.site.register(File, FileAdmin)
