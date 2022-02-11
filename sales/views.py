# Django
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
# App
from sales.models import Store, Item, Buyer


# Home Views

def index(request):
    messages.add_message(request, messages.INFO, 'Redirected to home')
    return HttpResponseRedirect(reverse('sales:home'))


def home(request):
    root_store = Store.objects.get(pk=1)
    # Items have to go in pairs to render blocks of (Black, White) (White, Black)...
    root_items = _get_pair_items(root_store.id)
    return render(request, 'sales/home.html', {'pair_items': root_items, 'store': root_store})


def checkout(request, item_id):
    item = Item.objects.get(pk=item_id)
    return render(request, 'sales/checkout.html', {'item': item})


def buy(request, item_id):
    item = Item.objects.get(pk=item_id)
    try:
        buyer = Buyer.objects.get(username=request.POST['username'])
    except Buyer.DoesNotExist:
        new_buyer = Buyer(username=request.POST['username'])
        new_buyer.save()
        item.buyers.add(new_buyer)
        messages.add_message(request, messages.INFO, f'Successfully bought {item.name}')
        return HttpResponseRedirect(reverse('sales:home'))
    else:
        item.buyers.add(buyer)
        messages.add_message(request, messages.INFO, f'Successfully bought {item.name}')
        return HttpResponseRedirect(reverse('sales:home'))


# Private Methods

def _get_pair_items(store_pk):
    store = Store.objects.get(pk=store_pk)
    pair_items = []
    for item in store.item_set.all():
        pair_items.append((item,))
    for i in range(len(pair_items)):
        try:
            pair_items[i] += pair_items[i+1]
            pair_items.pop(i+1)
        except IndexError:
            pass
    return pair_items
