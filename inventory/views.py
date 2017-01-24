from collections import OrderedDict
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
import json

from .forms import ItemForm, LoanForm, TagForm
from .models import Tag, Item, Loan


# TODO tekst på knapper må midtstilles
# TODO knapper må flyttes til bestemt punkt på skjermen
# TODO mulig å bruke QR-kode for merking av gjenstander, må føre til item sin detail-side

def index(request):
    items = Item.objects.all().filter(visible=True)
    no_category = []
    all_tags = [tag for tag in Tag.objects.all() if tag.item_set.all() and tag.visible]
    all_tags.sort(key=lambda tag: tag.name.lower())
    item_dict = OrderedDict()
    for sorted_tag in all_tags:
        item_dict[sorted_tag] = []
    for item in items:
        if not item.tags.all():
            no_category.append(item)

        for tag in item.tags.all():
            try:
                item_dict[tag].append(item)
            except KeyError:
                item_dict[tag] = [item]
    for value in item_dict.values():
        value.sort(key=lambda e: e.name.lower())
    no_category.sort(key=lambda w: w.name.lower())
    context = {
        'item_dict': item_dict,
        'no_category': no_category,
    }
    return render(request, 'inventory/index.html', context)


def search(request):
    search_text = request.GET['q']
    if search_text.strip() == '/all':
        context = {
            'hits': Item.objects.all().filter(visible=True),
            'search_text': search_text,
            'tags': Tag.objects.all().filter(visible=True).order_by('name')
        }
        return render(request, 'inventory/search.html', context)
    search_words = search_text.split()
    return_set = []
    tags = []
    for word in search_words:
        return_set += Item.objects.filter(visible=True).filter(tags__name__contains=word)
        return_set += Item.objects.filter(visible=True).filter(name__contains=word)
        return_set += Item.objects.filter(visible=True).filter(description__contains=word)
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


@permission_required(['inventory.add_item', 'inventory.change_item', 'inventory.add_tag'])
def add_item(request, item_id=0):
    message = "Legg til en ny gjenstand"  # TODO se om denne og button_message kan settes med javascript,
    # eller messages framework?
    button_message = "registrer"
    old_tags = []  # liste med alle tags en gjenstand har, for å fylle tags-feltet når man skal endre
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            # skiller ikke på store/små bokstaver itags
            if item_id != '0':  # existing item to be changed
                item = Item.objects.get(pk=item_id)
                """
                basic_attributes = ['name', 'description', 'quatity']
                for attr in basic_attributes:
                    setattr(item, attr, form.cleaned_data[attr])
                """
                item.name = form.cleaned_data['name']
                item.description = form.cleaned_data['description']
                item.quantity = form.cleaned_data['quantity']
                item.save()
                messages.add_message(request, messages.SUCCESS, 'Gjenstanden ble endret.')
            else:  # create new item from form
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                quantity = form.cleaned_data['quantity']
                item = Item(name=name, description=description, quantity=quantity)
                # item = Item(**form.cleaned_data)
                item.save()
                item_id = item.id
                messages.add_message(request, messages.SUCCESS, 'Gjenstandet ble opprettet')
            form.add_new_tags(item_id)
            return HttpResponseRedirect(reverse('inventory:index'))
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


@permission_required(['inventory.change_item', 'inventory.delete_item'])
def change_multiple_items(request):
    """ For å endre flere itmes, tilgjengelig hvis man merker gjenstander i search og trykker 'endre'. """
    # TODO søk på "arduino": hverken arduino eller OculusRift lar seg avmerke i boksen, det fungerer på resten
    # TODO endre her så man også kan lage nye tags
    if request.method == "POST":
        try:
            """ Items marked in search-view for changing """
            # items_for_changing: String of all item_id's to be changed, separated with '_' (also one at the end)
            items_for_changing = request.POST['items']
        except KeyError:
            form = ItemForm(request.POST)
            # TODO is_valid() returnerer ikke true
            form.is_valid()
            items = form.cleaned_data['tags_chips']
            try:
                new_tags = form.cleaned_data['name']
            except KeyError:
                """ Deletes all marked items """
                ItemForm.delete_all_items(items)
                messages.add_message(request, messages.SUCCESS, "Gjenstander ble slettet.")
                return HttpResponseRedirect(reverse('inventory:index'))
            else:
                """ Changes tag on all marked items """
                ItemForm.change_tags(items, new_tags)
                messages.add_message(request, messages.SUCCESS, "Tagger ble oppdatert.")
                return HttpResponseRedirect(reverse('inventory:index'))
        else:
            items = [get_object_or_404(Item, pk=item_id) for item_id in items_for_changing.split('_')[:-1]]
            context = {
                'autocomplete_dict': ItemForm.get_autocomplete_dict(),
                'form': ItemForm(initial={'tags_chips': items_for_changing, 'name': 'skip'}),
                'items': items,
            }
            return render(request, 'inventory/change_multiple_items.html', context)
    else:
        # TODO slags felles metode for dette i search-view?
        return render(request, 'inventory/search.html', {
            'hits': Item.objects.all().filter(visible=True).order_by('name'),
            'search_text': '/all',
            'tags': Tag.objects.all()
        })


@permission_required(['inventory.add_tag', 'inventory.change_tag'])
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
                messages.add_message(request, messages.SUCCESS, 'Taggen ble endret.')
                messages.add_message(request, messages.SUCCESS, 'Taggen ble endret.')
            else:
                name = form.cleaned_data['name']
                tag = Tag(name=name)
                tag.save()
                messages.add_message(request, messages.SUCCESS, 'Taggen ble opprettet.')
            return HttpResponseRedirect(reverse('inventory:index'))
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


def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    context = {
        'tag': tag,
        'related_items': tag.item_set.all().order_by('name'),
    }
    return render(request, 'inventory/tag_detail.html', context)


@permission_required('inventory.add_loan')
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
            messages.add_message(request, messages.SUCCESS, 'Lånet ble registrert')
            return HttpResponseRedirect(reverse('inventory:index'))
    else:
        form = LoanForm()
    return HttpResponse(render(request, 'inventory/register_loan.html', {'form': form}))


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
