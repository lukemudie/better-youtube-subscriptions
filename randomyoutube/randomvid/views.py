from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    """View function for home page of this site"""
    context = {
        'channel_id': 'UCHZqZf6nbTu3hnRtOJwUtkA'
    }
    
    return render(request, 'index.html', context=context)