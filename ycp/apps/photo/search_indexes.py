from haystack import indexes
from ycp.apps.photo.models import Photo

class PhotoIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Description: Haystack search index for Photo model
                             
    Author:      Nnoduka Eruchalu
    """
    
    text = indexes.EdgeNgramField(document=True, use_template=True)
    
    def get_model(self):
        return Photo

