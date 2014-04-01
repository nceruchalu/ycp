"""
Description: Helpful utility functions for youtube app

Author:      Nnoduka Eruchalu
"""

import re

def youtubeParser(url):
    """
    Description:
      extract and return video ID from following types of URLs:
        http://www.youtube.com/watch?v=0zM3nApSvMg&feature=feedrec_grec_index
        http://www.youtube.com/user/IngridMichaelsonVEVO#p/a/u/1/QdK8U-VIH_o
        http://www.youtube.com/v/0zM3nApSvMg?fs=1&amp;hl=en_US&amp;rel=0
        http://www.youtube.com/watch?v=0zM3nApSvMg#t=0m10s
        http://www.youtube.com/embed/0zM3nApSvMg?rel=0
        http://www.youtube.com/watch?v=0zM3nApSvMg
        http://youtu.be/0zM3nApSvMg
    
      if invalid url, return False
    
    Arguments: - url: YouTube URL to be parsed
    Return:    video_id if a valid video URL, else return False
    
    Author:    Nnoduka Eruchalu
    """
    prog = re.compile(
        r'^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=)([^#\&\?]*).*')
    match = prog.match(url)
    
    if (match and (len(match.groups()) == 2)):
        video_id = match.group(2)
        if (len(video_id) == 11):
            return video_id
    
    # invalid url    
    return False
