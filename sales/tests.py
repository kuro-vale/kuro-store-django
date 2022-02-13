# Django
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
# App
from django.utils import timezone

from sales.models import Buyer, Purchase


# Model Tests

class ItemModelTests(TestCase):
    def test_models_workflow(self):
        owner = User()
        owner.save()
        store = owner.store_set.create()
        item = store.item_set.create()
        buyer = Buyer()
        buyer.save()
        purchase = Purchase(buyer_id=buyer, item_id=item, date=timezone.now())
        purchase.save()
        self.assertEqual(store.item_set.get(pk=item.id), buyer.purchase_set.get(pk=1).item_id)


# View Tests

class HomeViewsTests(TestCase):
    def test_index_redirect_to_home(self):
        response = self.client.get(reverse('sales:index'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/home/')

    def test_root_items_got_render_in_home(self):
        owner = User()
        owner.save()
        store = owner.store_set.create()
        item = store.item_set.create(name='Test Django')
        response = self.client.get(reverse('sales:home'))
        self.assertContains(response, item.name)
