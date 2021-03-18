from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    """View function for home page of this site"""
    channel_id = 'UCHZqZf6nbTu3hnRtOJwUtkA'
    video_id = 'N7ENYEdP90w'
    embed_link = 'https://www.youtube.com/embed/' + video_id + '?&autoplay=1'
    
    context = {
        'channel_id': channel_id,
        'video_id': video_id,
        'embed_link': embed_link
    }
    
    return render(request, 'index.html', context=context)