# Django
from django.urls import path
# App
from sales import views

app_name = 'sales'
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('checkout/<int:item_id>', views.checkout, name='checkout'),
    path('dashboard/latest', views.latest_purchases, name='latest'),
    path('dashboard/buyer/<int:buyer_id>', views.buyer_purchases, name='buyer_purchases'),
    path('create-store', views.create_store, name='create_store'),
    path('stores', views.view_stores, name='stores'),
]
