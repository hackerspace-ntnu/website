from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Tag, Item, Loan
from .forms import ItemForm, LoanForm, TagForm


def index(request):
    items = Item.objects.all()
    # items.sort(key=lambda a: a.tags.get(pk=1))
    item_dict = {}
    no_category = []
    for item in items:
        if not item.tags.all():
            no_category.append(item)

        for tag in item.tags.all():
            try:
                item_dict[tag].append(item)
            except KeyError:
                item_dict[tag] = [item]

    for value in item_dict.values():
        value.sort(key=lambda e: e.name.title())

    context = {
        'item_dict': item_dict,
        'no_category': no_category,
    }
    return render(request, 'inventory/index.html', context)


def detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    context = {
        'item': Item.objects.get(pk=item_id)
    }
    return render(request, 'inventory/detail.html', context)


# @login_required
def add_item(request, id=None):

    if request.method == 'POST':
        form = ItemForm(request.POST)
        if id:
            # TODO eksisterende id skal bare endres, ikke lag ny
            item = Item.objects.get(pk=id)
            item.name = form.changed_data['name']


            pass

        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['descritption']
            quantity = form.cleaned_data['quantity']
            tags = form.cleaned_data['tags']

            item = Item(name=name, quantity=quantity, description=description)
            item.save()

            # TODO legge til at en liten melding vises øverst når man laster inn neste side, se: "the messages framwork"

            return HttpResponseRedirect(reverse('inventory:registered'))
    else:
        form = ItemForm()
        if id:
            # TODO eksisterende item skal endres, form må fylles med data
            pass

    return render(request, 'inventory/add_item.html', {'form': form})


def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            tag = Tag(name=name)
            tag.save()
            return HttpResponseRedirect(reverse('inventory:registered'))
    else:
        form = TagForm()

    return render(request, 'inventory/add_tag.html', {'form': form})


def loan(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data['item']
            borrower = form.cleaned_data['borrower']
            # TODO plukk ut bruker som var logget inn, og lagre i variabel lender
            comment = form.cleaned_data['comment']

            loan_date = timezone.now()
            return_date = form.cleaned_data['return_date']
            loan = Loan(item=item, borrower=borrower, comment=comment, loan_date=loan_date, return_date=return_date)
            loan.save()
            return HttpResponseRedirect(reverse('inventory:registered'))
    else:
        form = LoanForm()
    return HttpResponse(render(request, 'inventory/loan.html', {'form': form}))


def change_item(request, item_id):
    return HttpResponse("endre objekt")


def registered(request):
    name = "NAME"
    return HttpResponse("Din " + name + " ble registert." + '<a href="/inventory/">link</a> ')
