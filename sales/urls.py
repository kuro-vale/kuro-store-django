# Django
from django.urls import path
# App
from sales import views

app_name = 'sales'
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('checkout/<int:item_id>/', views.checkout, name='checkout'),
    path('dashboard/latest/', views.latest_purchases, name='latest'),
    path('dashboard/buyer/<int:buyer_id>/', views.buyer_purchases, name='buyer_purchases'),
    path('stores/create/', views.create_store, name='create_store'),
    path('stores/', views.view_stores, name='stores'),
    path('stores/<int:store_id>/', views.user_store, name='user_store'),
    path('items/add/<int:store_id>/', views.add_item, name='add_item'),
    path('items/edit/<int:item_id>/', views.edit_item, name='edit_item'),
    path('items/delete/<int:item_id>/', views.delete_item, name='delete_item')
]
