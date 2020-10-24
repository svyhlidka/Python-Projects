from django import forms  #new
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

class NewTaskForm(forms.Form):
  #  define all fields
    task = forms.CharField(label="New Task")
    priority = forms.IntegerField(label="Priority",min_value=1,max_value=5)

# before sessions tasks = ['task1','task2','task3']  # global var

def indexBeforeSessions(request):
    return render(request, 'tasks/index.html', {
             "tasks": tasks  
        })

def index(request):
   if "tasks" not in request.session:
       request.session["tasks"] = []
        
   return render(request, 'tasks/index.html', {
             "tasks": request.session["tasks"] 
    })
   
      
def addOrig(request):
    return render(request, 'tasks/add.html', {
         "tasks": tasks  
    })

def add1(request):
    return render(request, 'tasks/add.html', {
         "form": NewTaskForm()  
    })

def add(request):
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():                 # if data is valid
            task = form.cleaned_data["task"] #takes data from the form
            request.session["tasks"] += [task]
            #if we want to redirect back
            return HttpResponseRedirect(reverse('tasks:index')) #this not
        else:
            return render(request, "tasks/add.html", {
                "form": form
            })
        
    return render(request, 'tasks/add.html', {
         "form": NewTaskForm()  
    })