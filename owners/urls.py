# Django
from django.urls import path
# App
from owners import views

app_name = 'auth'
urlpatterns = [
    path('logout/', views.logout_owner, name='logout'),
    path('login/', views.render_login, name='login'),
    path('login_owner/', views.login_owner, name='login_owner')
]
