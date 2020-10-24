
from django.shortcuts import render
from django.http import request, JsonResponse
import time
# Create your views here.


def index(request):
    return render(request,"posts/index.html")
# 127.0.0.1:8000/posts/?start=1&end=10


def posts(request):

    
    # data = [{'name': 'Peterwwwww', 'email': 'peter@example.org'},
    #       {'name': 'Julia', 'email': 'julia@example.org'}]

    # return JsonResponse(data, safe=False)
    
    #  Get start and end points
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 9))
    
    # Generate list of posts
    data = []
    for i in range(start, end+1):

        data.append(f'Post #{i}')
    
    # Artifically delay speed of response
    time.sleep(1)
    
    # Return list of posts
    return JsonResponse({"posts": data}, safe=False)
    