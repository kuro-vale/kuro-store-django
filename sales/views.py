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
    if request.user.is_authenticated:
        if not request.user.store_set.all():
            pass
        else:
            return HttpResponseRedirect(reverse('sales:user_home'))
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


def store_purchases(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    purchases = None
    for item in store.item_set.all():
        purchases = Purchase.objects.filter(item_id=item)
        break
    return render(request, 'sales/dashboards/store.html', {'store': store, 'purchases': purchases})


# Store Views

@login_required(login_url='auth/login')
def create_store(request):
    view_name = 'Create A New Store'
    if request.method == 'POST':
        store = Store(name=request.POST['store-name'], description=request.POST['description'], owner=request.user)
        store.save()
        messages.add_message(request, messages.SUCCESS, f'{store.name} Successfully Created')
        return HttpResponseRedirect(reverse('sales:home'))
    return render(request, 'sales/create_store.html', {'view_name': view_name})


def view_stores(request):
    view_name = 'User Stores'
    stores = Store.objects.filter(pk__gt=1)
    return render(request, 'sales/stores.html', {'stores': stores, 'view_name': view_name})


def user_store(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    items = _get_pair_items(store.id)
    return render(request, 'sales/home.html', {'pair_items': items, 'store': store})


# Item Views

@login_required(login_url='auth/login')
def add_item(request, store_id):
    view_name = 'Add Item'
    store = get_object_or_404(Store, pk=store_id)
    if not store.owner == request.user:
        return HttpResponseRedirect(reverse('sales:home'))
    if request.method == 'POST':
        name = request.POST['item-name']
        description = request.POST['description']
        image = request.POST['image']
        price = request.POST['price']
        item = Item(store_id=store, name=name, description=description, image=image, price=price)
        item.save()
        messages.add_message(request, messages.SUCCESS, f'{item.name} Successfully Added')
        return HttpResponseRedirect(reverse('sales:home'))
    return render(request, 'sales/add_item.html', {'view_name': view_name})


@login_required(login_url='auth/login')
def edit_item(request, item_id):
    view_name = 'Edit Item'
    item = get_object_or_404(Item, pk=item_id)
    if not item.store_id.owner == request.user:
        return HttpResponseRedirect(reverse('sales:home'))
    if request.method == 'POST':
        item.name = request.POST['item-name']
        item.description = request.POST['description']
        item.image = request.POST['image']
        item.price = request.POST['price']
        item.save()
        messages.add_message(request, messages.SUCCESS, f'{item.name}Successfully Updated')
        return HttpResponseRedirect(reverse('sales:home'))
    return render(request, 'sales/add_item.html', {'view_name': view_name})


@login_required(login_url='auth/login')
def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if not item.store_id.owner == request.user:
        return HttpResponseRedirect(reverse('sales:home'))
    item.delete()
    messages.add_message(request, messages.WARNING, f'{item.name} Was Deleted')
    return HttpResponseRedirect(reverse('sales:home'))


# User Views

@login_required(login_url='auth/login')
def user_home(request):
    view_name = 'Your Stores'
    stores = Store.objects.filter(owner=request.user)
    return render(request, 'sales/stores.html', {'stores': stores, 'view_name': view_name})


@login_required(login_url='auth/login')
def edit_store(request, store_id):
    view_name = 'Edit Store'
    store = get_object_or_404(Store, pk=store_id)
    if not store.owner == request.user:
        return HttpResponseRedirect(reverse('sales:home'))
    if request.method == 'POST':
        store.name = request.POST['store-name']
        store.description = request.POST['description']
        store.save()
        messages.add_message(request, messages.SUCCESS, f'{store.name} Successfully Edited')
        return HttpResponseRedirect(reverse('sales:home'))
    return render(request, 'sales/create_store.html', {'view_name': view_name})


@login_required(login_url='auth/login')
def delete_store(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    if not store.owner == request.user:
        return HttpResponseRedirect(reverse('sales:home'))
    store.delete()
    messages.add_message(request, messages.WARNING, f'{store.name} Was Deleted')
    return HttpResponseRedirect(reverse('sales:home'))


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
