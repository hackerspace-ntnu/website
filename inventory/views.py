from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Tag, Item, Loan
from .forms import ItemForm, LoanForm, TagForm
import json


# TODO tekst på knapper må midtstilles
# TODO knapper må flyttes til bestemt punkt på skjermen
# TODO mulig å bruke QR-kode for merking av gjenstander, må føre til item sin detail-side
# TODO alt må endres slik at kun de som er innlogget og er i hackerspace har tilgang til å endre osc.

def index(request):
    items = Item.objects.all()
    item_dict = {}  # TODO vurdere å bytte ut med en sorted dict for å kunne vise kategoriene sortert,
    # evt legge kategorier i en sortert liste
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
    no_category.sort(key=lambda w: w.name.lower())
    context = {
        'item_dict': item_dict,
        'no_category': no_category,
    }
    return render(request, 'inventory/index.html', context)


def search(request):
    search_text = request.GET['q']
    search_words = search_text.split()
    return_set = []
    tags = []
    for word in search_words:
        return_set += Item.objects.filter(tags__name__contains=word)
        return_set += Item.objects.filter(name__contains=word)
        tags += Tag.objects.filter(name__contains=word)

    return_set = list(set(return_set))
    return_set.sort(key=lambda i: i.name.lower())

    context = {
        'hits': return_set,
        'search_text': search_text,
        'tags': tags,
    }
    return render(request, 'inventory/search.html', context)


def detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, 'inventory/detail.html', {'item': item})


# @login_required  # TODO tilgjenelighet må endres mtp om man er innlogget eller ikke
def add_item(request, item_id=0):
    message = "Legg til en ny gjenstand"  # TODO se om denne og button_message kan settes med javascript
    button_message = "registrer"
    old_tags = []  # liste med alle tags en gjenstand har, for å fylle tags-feltet når man skal endre
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            # skiller ikke på store/små bokstaver itags
            if item_id != '0':  # existing item to be changed
                item = Item.objects.get(pk=item_id)
                item.name = form.cleaned_data['name']
                item.description = form.cleaned_data['description']
                item.quantity = form.cleaned_data['quantity']
                item.save()
            else:  # create new item from form
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                quantity = form.cleaned_data['quantity']
                item = Item(name=name, description=description, quantity=quantity)
                item.save()
                item_id = item.id
            form.add_new_tags(item_id)
            # TODO legge til at en liten melding vises øverst når man laster inn neste side, se: "the messages framwork"
            return HttpResponseRedirect(reverse('inventory:registered'))
    else:
        form = ItemForm()
        if item_id:
            message = "Endre gjenstand"
            button_message = "endre"
            item = Item.objects.get(pk=item_id)
            old_tags = []
            for tag in item.tags.all():
                auto_comp_dict = {'id': tag.id, 'text': tag.name}
                old_tags.append(auto_comp_dict)
            initial = {
                'name': item.name,
                'description': item.description,
                'quantity': item.quantity,
            }
            form = ItemForm(initial=initial)
    context = {
        'form': form,
        'message': message,
        'button_message': button_message,
        'item_id': item_id,
        'old_tags': json.dumps(old_tags),
    }
    return render(request, 'inventory/add_item.html', context)


# @login_required  # TODO tilgjenelighet må endres mtp om man er innlogget eller ikke
def add_tag(request, tag_id=0):
    message = "Legg til ny tag"
    button_message = "Legg til"

    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            if tag_id != '0':  # form sender streng tilbake, selv om den passes som inten 0 i context
                tag = Tag.objects.get(pk=tag_id)
                tag.name = form.cleaned_data['name']
                tag.save()
            else:
                name = form.cleaned_data['name']
                tag = Tag(name=name)
                tag.save()

            # TODO legge til at en liten melding vises øverst når man laster inn neste side, se: "the messages framwork"
            return HttpResponseRedirect(reverse('inventory:registered'))
    else:
        form = TagForm()
        if tag_id:
            message = "Endre tag"
            button_message = "Endre"
            tag = Tag.objects.get(pk=tag_id)
            form = TagForm(initial={'name': tag.name})

    context = {
        'form': form,
        'message': message,
        'button_message': button_message,
        'tag_id': tag_id,
    }
    return render(request, 'inventory/add_tag.html', context)


# @login_required  # TODO tilgjenelighet må endres mtp om man er innlogget eller ikke
def register_loan(request):
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
    return HttpResponse(render(request, 'inventory/register_loan.html', {'form': form}))


def registered(request):
    name = "NAME"
    # TODO mulig å heller redirecte til index, og ha en toast som sier at item.name er registrert, må da finne en
    # måte å vise denne toasten selv om man kommer til ny side
    # TODO kan evt vise toast og så redirecte etter et par sekunder
    return render(request, 'inventory/registered.html', {'type': name})


def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    related_items = list(tag.item_set.all())
    related_items.sort(key=lambda i: i.name.lower())
    context = {
        'tag': tag,
        'related_items': related_items,
    }
    return render(request, 'inventory/tag_detail.html', context)


def loans(request):
    '''return HttpResponse("liste over nåværende, for sene og gamle utlån")'''

    all_loans = Loan.objects.all()
    current_loans = all_loans.filter(date_returned__isnull=True).filter(return_date__lte=timezone.now()).order_by(
        'loan_date')
    late_loans = all_loans.filter(date_returned__isnull=True).filter(return_date__gte=timezone.now()).order_by(
        'loan_date')
    old_loans = all_loans.filter(date_returned__isnull=False).order_by('date_returned')

    context = {
        'current_loans': current_loans,
        'late_loans': late_loans,
        'old_loans': old_loans,
    }

    return render(request, 'inventory/loans.html', context)


def loan_detail(request, id):
    return HttpResponse("detaljer for utlån med id " + str(id))
