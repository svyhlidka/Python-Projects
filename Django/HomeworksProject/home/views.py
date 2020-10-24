from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import  User
from django.core.exceptions import ObjectDoesNotExist

from home.forms import HomeForm
from home.models import Post, Friend

class HomeView(TemplateView):
    template_name = 'home/home.html'
    
    def get(self,request):
        form = HomeForm()
        posts = Post.objects.all()
        users = User.objects.exclude(id=request.user.id)
        # friend is object many-to-many i.e. contains list of user objects
        try:
            friend = Friend.objects.get(current_user=request.user)
            friends = friend.users.all()
        except ObjectDoesNotExist:
            friends = None
        
        args = {'form':form, 'posts':posts, 'users': users, 'friends': friends}
        return render(request, self.template_name, args)
 
    
    def post(self, request):
        form = HomeForm(request.POST) # form initialization - blank
        if form.is_valid():
            post = form.save(commit=False) # before commit we want to make some change
            post.user = request.user
            post.save()
            
            text = form.cleaned_data['post']
            form = HomeForm() # <= this cleans data in the form
            return redirect('home:home') 
        args = {'form':form, 'text':text}
        return render(request, self.template_name, args)

def change_friends(request, operation, pk):
    friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
    return redirect('home:home')
    