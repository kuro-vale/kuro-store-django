# Django
from django.urls import path
# App
from owners import views

app_name = 'auth'
urlpatterns = [
    path('logout/', views.logout_owner, name='logout'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
]
