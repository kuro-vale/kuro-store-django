from django.contrib.auth.models import User
from django.db import models


class Buyer(models.Model):
    username = models.TextField(default='buyer')

    def __str__(self):
        return f'{self.username}'


class Store(models.Model):
    name = models.TextField(default='store')
    description = models.TextField(default='store')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


class Item(models.Model):
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.TextField(default='item', max_length=30)
    description = models.TextField(default='', blank=True, max_length=60)
    image = models.URLField(max_length=200)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.name}'


class Purchase(models.Model):
    buyer_id = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    date = models.DateField('Date Purchased')

    def __str__(self):
        return f'Purchase of {self.item_id.name} by {self.buyer_id.username}'
