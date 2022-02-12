from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


# Auth Views

def render_login(request):
    return render(request, 'owners/login.html')


def login_owner(request):
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


def logout_owner(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Successfully logout')
    return HttpResponseRedirect(reverse('sales:home'))
