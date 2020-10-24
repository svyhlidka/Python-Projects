
from django.shortcuts import render
from django.http import request, JsonResponse
import time
# Create your views here.
def index(request):
    return render(request,"posts/index.html")
# 127.0.0.1:8000/posts/?start=1&end=10


def posts(request):
    
    data = [{'name': 'Peter', 'email': 'peter@example.org'},
          {'name': 'Julia', 'email': 'julia@example.org'}]

    return JsonResponse(data, safe=False)


