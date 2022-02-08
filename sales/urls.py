from django.urls import path

from sales import views

app_name = 'sales'
urlpatterns = [
    path('home/', views.home, name='home')
]
