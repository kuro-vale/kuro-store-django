from django.urls import path

from sales import views

app_name = 'sales'
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('checkout/<int:item_id>', views.checkout, name='checkout'),
    path('buy/<int:item_id>', views.buy, name='buy')
]
