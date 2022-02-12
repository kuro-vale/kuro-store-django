# Django
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
# App
from sales.models import Buyer, Item


# Model Tests

class ItemModelTests(TestCase):
    def test_item_have_1_store_and_multiple_buyers(self):
        owner = User()
        owner.save()
        store = owner.store_set.create()
        item = store.item_set.create()
        buyer1 = Buyer()
        buyer1.save()
        buyer2 = Buyer()
        buyer2.save()
        item.buyers.add(buyer1, buyer2)
        self.assertQuerysetEqual(store.item_set.all(), Item.objects.all())
        self.assertQuerysetEqual(buyer1.item_set.all(), Item.objects.all())
        self.assertEqual(item.buyers.get(pk=buyer2.pk), Buyer.objects.get(pk=buyer2.pk))


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
