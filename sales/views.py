from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def index(request):
    return HttpResponseRedirect(reverse('sales:home'))


def home(request):
    return render(request, 'sales/home.html')
