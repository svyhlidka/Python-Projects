from django.shortcuts import render
from django.http import Http404, HttpResponse

# Create your views here.

def index(request):
    return render(request, "singlepage/index.html")

texts = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit.  ",
         "Praesent sed euismod erat. Donec elementum tortor eget turpis sodales aliquam.",
         "Curabitur arcu justo, lobortis tempor turpis quis, feugiat tristique lacus. "]

def section(request, num):
    if 1 <= num <=3:
        
        return HttpResponse(texts[num-1])
    else:
        raise Http404("No such section")
        
        