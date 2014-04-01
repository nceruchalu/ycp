from haystack import indexes
from ycp.apps.blog.models import Post

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Description: Haystack search index for Post model
                             
    Author:      Nnoduka Eruchalu
    """
    
    text = indexes.EdgeNgramField(document=True, use_template=True)
    
    def get_model(self):
        return Post

