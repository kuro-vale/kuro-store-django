from django.shortcuts import render


def home(request):
    return render(request, 'sales/home.html')

