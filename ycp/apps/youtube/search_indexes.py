from haystack import indexes
from ycp.apps.youtube.models import Video

class VideoIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Description: Haystack search index for Video model
                             
    Author:      Nnoduka Eruchalu
    """
    
    text = indexes.EdgeNgramField(document=True, use_template=True)
    
    def get_model(self):
        return Video

