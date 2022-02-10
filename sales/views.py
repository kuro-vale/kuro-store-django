from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from sales.models import Store


def index(request):
    return HttpResponseRedirect(reverse('sales:home'))


def home(request):
    root_store = Store.objects.get(pk=1)
    # Items have to go in pairs to render blocks of (Black, White) (White, Black)...
    root_items = [range(1, 3), range(3, 5), range(5, 7), range(7, 8)]
    return render(request, 'sales/home.html', {'items': root_items, 'store': root_store})
