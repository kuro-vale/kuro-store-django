# Django
from django.contrib import admin
# App
from sales.models import Item, Store, Buyer

admin.site.register(Buyer)
admin.site.register(Store)
admin.site.register(Item)
