from django.contrib import messages
from django.contrib.auth import logout, authenticate, login, hashers
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


# Auth Views

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        owner = authenticate(request, username=username, password=password)
        if owner is not None:
            login(request, owner)
            messages.add_message(request, messages.SUCCESS, f'Welcome {username}')
            return HttpResponseRedirect(reverse('sales:home'))
        else:
            messages.add_message(request, messages.WARNING, 'Invalid Information')
            return HttpResponseRedirect(reverse('auth:login'))
    return render(request, 'owners/login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        hash_password = hashers.make_password(password)
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            owner = User(username=username, password=hash_password)
            owner.save()
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.add_message(request, messages.SUCCESS, f'{username} Successfully Created')
            return HttpResponseRedirect(reverse('sales:home'))
        else:
            messages.add_message(request, messages.WARNING, f'{username} Already Exist, Please Try Another Username')
            return HttpResponseRedirect(reverse('auth:signup'))
    return render(request, 'owners/signup.html')


def logout_owner(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Successfully logout')
    return HttpResponseRedirect(reverse('sales:home'))
