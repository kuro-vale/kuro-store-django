# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
# App
from sales.models import Store, Item, Buyer, Purchase


# Home Views

def index(request):
    messages.add_message(request, messages.INFO, 'Redirected to home')
    return HttpResponseRedirect(reverse('sales:home'))


def home(request):
    root_store = Store.objects.get(pk=1)
    root_items = _get_pair_items(root_store.id)
    return render(request, 'sales/home.html', {'pair_items': root_items, 'store': root_store})


# Buy views

def checkout(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        try:
            buyer = Buyer.objects.get(username=request.POST['username'])
        except Buyer.DoesNotExist:
            new_buyer = Buyer(username=request.POST['username'])
            new_buyer.save()
            purchase = Purchase(buyer_id=new_buyer, item_id=item, date=timezone.now())
            purchase.save()
            messages.add_message(request, messages.INFO, f'Successfully bought {item.name}')
            return HttpResponseRedirect(reverse('sales:home'))
        else:
            purchase = Purchase(buyer_id=buyer, item_id=item, date=timezone.now())
            purchase.save()
            messages.add_message(request, messages.INFO, f'Successfully bought {item.name}')
            return HttpResponseRedirect(reverse('sales:home'))
    return render(request, 'sales/checkout.html', {'item': item})


# Dashboard views

def latest_purchases(request):
    purchases = Purchase.objects.all()
    return render(request, 'sales/dashboards/latest.html', {'purchases': purchases})


def buyer_purchases(request, buyer_id):
    buyer = get_object_or_404(Buyer, pk=buyer_id)
    return render(request, 'sales/dashboards/buyer.html', {'buyer': buyer})


# Store Views

@login_required(login_url='auth/login')
def create_store(request):
    if request.method == 'POST':
        store = Store(name=request.POST['store-name'], description=request.POST['description'], owner=request.user)
        store.save()
        messages.add_message(request, messages.SUCCESS, f'{store.name} Successfully Created')
        return HttpResponseRedirect(reverse('sales:home'))
    return render(request, 'sales/create_store.html')


def view_stores(request):
    stores = Store.objects.filter(pk__gt=1)
    store_scope = 'User Stores'
    return render(request, 'sales/stores.html', {'stores': stores, 'store_scope': store_scope})


def user_store(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    items = _get_pair_items(store.id)
    return render(request, 'sales/home.html', {'pair_items': items, 'store': store})


@login_required(login_url='auth/login')
def add_item(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    if request.method == 'POST':
        name = request.POST['item-name']
        description = request.POST['description']
        image = request.POST['image']
        price = request.POST['price']
        item = Item(store_id=store, name=name, description=description, image=image, price=price)
        item.save()
        messages.add_message(request, messages.SUCCESS, f'{item.name} Successfully Added')
        return HttpResponseRedirect(reverse('sales:home'))
    return render(request, 'sales/add_item.html')


# Private Methods

def _get_pair_items(store_pk):
    """Items have to go in pairs to render blocks of (Black, White) (White, Black)...and so"""
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
