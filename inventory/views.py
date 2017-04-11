from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import View

import json

from .forms import ItemForm, LoanForm, TagForm
from .models import Tag, Item, Loan


# TODO mulig å bruke QR-kode for merking av gjenstander, må føre til item sin detail-side
# TODO hvordan skal man gjøre det med gjenstander som er slettet (not visible), skal de kunne gjenopprettes?
# TODO DIGER BUG! Skjekk at tagen man prøver å sette som forelder ikke ligger under i treet.
def index(request):
    items = Item.objects.filter(visible=True)
    posted_tags = {}

    if request.method == 'POST':
        result = json.loads(request.POST['check_json'])
        posted_tags = json.dumps(result)

        def parse_dict(tag_dict: dict):
            filtered_items = Item.objects.none()

            for tag_id, children in tag_dict.items():
                # Må legge til items for alle tags på samme nivå
                related_items = Tag.objects.get(pk=tag_id).item_set.filter(visible=True).all()
                if children:
                    # Hvis tagen har barn, skal man bare ta med items som er taget med begge
                    filtered_items |= related_items & parse_dict(children)
                else:
                    # legge til alle Items som hører til denne tagen tag_id
                    filtered_items |= related_items
            return filtered_items

        if result:
            items = parse_dict(result)

    context = {'items': items,
               'tags': Tag.objects.filter(parent_tag=None),
               'posted_tags': posted_tags  # For å checke av boksene som var checked når man refresher
               }

    return render(request, 'inventory/index.html', context)


def search(request):
    # TODO denne må oppdateres slik at den tar hensyn til subtags

    search_text = request.GET['q']
    if search_text.strip() == '/all':
        return render(request, 'inventory/search.html', show_all_items())
    search_words = search_text.split()
    return_set = []
    tags = []
    for word in search_words:
        return_set += Item.objects.filter(visible=True).filter(tags__name__contains=word)
        return_set += Item.objects.filter(visible=True).filter(name__contains=word)
        return_set += Item.objects.filter(visible=True).filter(description__contains=word)
        tags += Tag.objects.filter(name__contains=word)

    for tag in tags:
        return_set += tag.item_set.all().filter(visible=True)

    return_set = list(set(return_set))
    return_set.sort(key=lambda i: i.name.lower())

    context = {
        'hits': return_set,
        'search_text': search_text,
        'tags': tags,
    }
    return render(request, 'inventory/search.html', context)


def show_all_items() -> dict:
    """ Returns context with every item. """
    items = list(Item.objects.all().filter(visible=True))
    items.sort(key=lambda i: i.name.upper())

    return {
        'hits': items,
        'search_text': '/all',
        'tags': Tag.objects.all()
    }


def detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        item.visible = False
        item.save()
        messages.add_message(request, messages.SUCCESS, 'Gjenstanden ble slettet.')
        return HttpResponseRedirect(reverse('inventory:index'))
    return render(request, 'inventory/detail.html', {'item': item})


@permission_required(['inventory.add_item', 'inventory.change_item', 'inventory.add_tag'])
def add_item(request, item_id=0):
    message = "Legg til en ny gjenstand"
    button_message = "registrer"
    old_tags = []  # liste med alle tags en gjenstand har, for å fylle tags-feltet når man skal endre
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            # skiller ikke på store/små bokstaver itags
            if item_id != '0':  # existing item to be changed
                item = Item.objects.get(pk=item_id)
                basic_attributes = ['name', 'description', 'quantity', 'zone', 'shelf', 'place']
                for attr in basic_attributes:
                    setattr(item, attr, form.cleaned_data[attr])
                item.save()
                messages.add_message(request, messages.SUCCESS, 'Gjenstanden ble endret.')
            else:  # create new item from form
                item = Item(name=form.cleaned_data['name'],
                            description=form.cleaned_data['description'],
                            quantity=form.cleaned_data['quantity'],
                            zone=form.cleaned_data['zone'],
                            shelf=form.cleaned_data['shelf'],
                            place=form.cleaned_data['place'],
                            )
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
                'zone': item.zone,
                'shelf': item.shelf,
                'place': item.place,
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
    # TODO endre så man kan endre zone og/eller shelf
    # TODO lag en form og gjør viewet lesbart.
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
        return render(request, 'inventory/search.html', show_all_items())


# TODO permission_required redirecter ikke til dit man kom fra når man må logge inn
# TODO gjør så man kan sette sone og hylle for alle items med denne tagen.
# TODO lag mulighet til å slette en tag. Da bør denne gjøres class-based, og bruke delete-metoden
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
            else:
                name = form.cleaned_data['name']
                tag = Tag(name=name)
                tag.save()
                messages.add_message(request, messages.SUCCESS, 'Taggen ble opprettet.')

            this_id, parent_tag_id = json.loads(form.cleaned_data['parent_tag_ids'])
            parent_tag_id = 0 if parent_tag_id is None else parent_tag_id
            TagForm.add_parent_tag(tag.id, parent_tag_id)

            return HttpResponseRedirect(reverse('inventory:index'))
    else:
        form = TagForm()
        if int(tag_id) != 0:
            message = "Endre tag"
            button_message = "Endre"
            tag = Tag.objects.get(pk=tag_id)
            form = TagForm(initial={'name': tag.name})

    context = {
        'form': form,
        'message': message,
        'button_message': button_message,
        'tag_id': tag_id,
        'parent_tags_autocomplete': ItemForm.get_autocomplete_dict(),
        'parent_tag': {},
    }

    if int(tag_id) > 0:
        tag = Tag.objects.get(pk=tag_id)
        if tag.parent_tag is not None:
            parent_tag = {'id': tag.parent_tag.id, 'text': tag.parent_tag.name}
            context['parent_tag'] = json.dumps(parent_tag)

    return render(request, 'inventory/add_tag.html', context)


def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    context = {
        'tag': tag,
        'related_items': tag.item_set.all().filter(visible=True).order_by('name'),
    }
    return render(request, 'inventory/tag_detail.html', context)


class RegisterLoan(View):
    """ @permission_required('inventory.add_loan') er satt i urls.py """

    context = {
        'chosen_item': {}
    }

    def get(self, request, item_id=0):
        self.context['form'] = LoanForm()

        if int(item_id) > 0:
            item = Item.objects.get(pk=item_id)
            self.context['chosen_item'] = {'id': item.id, 'text': item.name}

        return HttpResponse(render(request, 'inventory/register_loan.html', self.context))

    def post(self, request, item_id=0):
        form = LoanForm(data=request.POST)
        if form.is_valid():
            loanitems = form.cleaned_data['items']
            del form.cleaned_data['items']

            loan = Loan.objects.create(**form.cleaned_data)
            loan.loanitem_set.add(*loanitems)
            loan.lender = request.user
            loan.loan_date = timezone.now()
            loan.save()

            messages.add_message(request, messages.SUCCESS, 'Lånet ble registrert')
            return HttpResponseRedirect(reverse('inventory:index'))

        self.context['form'] = form
        return HttpResponse(render(request, 'inventory/register_loan.html', self.context))


@permission_required('inventory.add_loan')
def administrate_loans(request):
    """ return HttpResponse("liste over nåværende, for sene og gamle utlån") """

    all_loans = Loan.objects.all().filter(date_returned__isnull=True)
    current_loans = all_loans.filter(return_date__gte=timezone.now()).order_by('loan_date')
    late_loans = all_loans.filter(return_date__lte=timezone.now()).order_by('loan_date')
    old_loans = Loan.objects.all().filter(date_returned__isnull=False).order_by('date_returned')

    context = {
        'current_loans': current_loans,
        'late_loans': late_loans,
        'old_loans': old_loans,
    }
    return render(request, 'inventory/administrate_loans.html', context)


@login_required
def my_loans(request):
    user = request.user
    loans = user.loan_set.all()
    context = {
        'loans': loans,
    }
    return render(request, 'inventory/my_loans.html', context)


@permission_required(['inventory.add_loan', 'inventory.change_loan', 'inventory.delete_loan'])
def loan_detail(request, loan_id):
    loan = get_object_or_404(Loan, pk=loan_id)
    if request.method == 'POST':
        if not loan.date_returned:
            loan.date_returned = timezone.now()
        else:
            loan.date_returned = None
        loan.save()
        return HttpResponseRedirect(reverse('inventory:loan_detail', args=(loan.id,)))

    return render(request, 'inventory/loan_detail.html', {'loan': loan})

# TODO listener for å sende ut mail med purring når det har gått litt over fristen, ..?
