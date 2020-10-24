from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.views import (LoginView,)
from django.contrib.auth.forms import (
                                       UserChangeForm, 
                                       UserCreationForm, 
                                       PasswordChangeForm
                                       )
from django.contrib.auth import update_session_auth_hash                                 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from accounts.forms import RegistrationForm, EditProfileForm
                     


# Create your views here.



#from users.models import User

    
def register(request):
    if request.method == 'POST':
        #form = UserCreationForm(request.POST)
        # there is customized version of UserCreationForm in forms.py 
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('home:home'))
    # else is for GET i.e. intialize a blank form
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'accounts/reg_form.html', args)

#@login_required    
def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    # i.e. if None user = default user, othewise finding user by pk
    args = {'user': user}
    return render(request, 'accounts/view_profile.html', args)

#@login_required
def edit_profile(request):
    
    if request.method == 'POST':
        #form = UserChangeForm(request.POST, instance=request.user)
        form = EditProfileForm(request.POST, instance=request.user)
        # instance -  
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:profile'))
    else:
    # else is for GET i.e. intialize a blank form
        #form = UserChangeForm(instance = request.user)
        form = EditProfileForm(instance = request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)

#@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
#        form = PasswordChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('accounts:profile'))
        else:
            return redirect(reverse('accounts:change_password'))
    # else is for GET i.e. intialize a blank form
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)

def password_reset_confirm(request):
    return render(request, 'accounts/password_reset_confirm.html')     