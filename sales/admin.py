# Django
from django.contrib import admin
# App
from sales.models import Item, Store, Buyer, Owner

admin.site.register(Owner)
admin.site.register(Buyer)
admin.site.register(Store)
admin.site.register(Item)
