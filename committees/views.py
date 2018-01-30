from dal import autocomplete
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

from .forms import CommitteeEditForm
from .models import Committee, Position
from files.models import Image


def index(request):
    committees = Committee.objects.prefetch_related('user_set')

    context = {
        'committees': committees,
    }

    return render(request, 'committees/list_committees.html', context)

def view_committee(request, name):
    committee = get_object_or_404(Committee, name=name)

    can_edit = edit_check(request.user, name)

    positions = Position.objects.filter(pos_in_committee=committee)
    pos_names = [p.usr.username for p in positions]

    users = [user for user in committee.user_set.all() if user.username not in pos_names]
    #users = filter(lambda user: user.username not in pos_names, committee.user_set.all())
    users.sort(key=lambda user: user.first_name)

    context = {
        'committee': committee,
        'can_edit': can_edit,
        'users': users,
        'positions': positions,
    }
    return render(request, 'committees/view_committee.html', context)

def edit_check(user, c_name):
    committee = get_object_or_404(Committee, name=c_name)
    return user.has_perm('can_edit_committees') or user in committee.admins.all()

def edit_members(request, committee_name):
    if edit_check(request.user, committee_name):
        if request.method == 'POST':
            if request.POST['action'] == 'add':
                json = add_member(request, committee_name)
            elif request.POST['action'] == 'delete':
                json = delete_member(request, committee_name)
            return json
        else:
            committee = get_object_or_404(Committee, name=committee_name)

            context = {
                'committee': committee,
                'usernames': [user.username for user in committee.user_set.all()],
                'all_users': User.objects.all(),
            }

            return render(request, 'committees/edit_members.html', context)
    else:
        return HttpResponseForbidden()

def add_member(request, com_name):
    try:
        user_string = request.POST['name']
        username = user_string.split("-")[-1].strip()
        user = User.objects.get(username=username)
        committee = Committee.objects.get(name=com_name)
        name = username

        if not user in committee.user_set.all():
            committee.add_user(user)
            committee.save()
            message = name + ' er nå med i ' + committee.name
        else:
            message = name + ' er allerede med i ' + committee.name

        return JsonResponse({'success': True, 'message': message, 'username': username}, safe=False)

    except IndexError:
        return JsonResponse({'success': False, 'message': 'Fant ikke bruker'}, safe=False)

def delete_member(request, com_name):
    try:
        username = request.POST['name']
        print(username)
        user = User.objects.get(username=username)
        committee = Committee.objects.get(name=com_name)
        name = username

        if user in committee.user_set.all():
            committee.remove_user(user)
            committee.save()
            message = name + ' er ikke lenger med i ' + committee.name
        else:
            message = name + ' er ikke med i ' + committee.name

        return JsonResponse({'success': True, 'message': message, 'username': username}, safe=False)

    except IndexError:
        return JsonResponse({'success': False, 'message': 'Fant ikke bruker'}, safe=False)
"""
def edit_committee(request, committee_name):
    committee = get_object_or_404(Committee, name=committee_name)
    form = EditDescription(request.POST or None, instance=committee)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.add_message(request, messages.SUCCESS, '{} har blitt endret!'.format(committee.name), extra_tags='Supert')
            return HttpResponseRedirect('/committees')
    context = {
        'committee': committee,
        'form': form,
    }
    return render(request, 'committees/edit_committee.html', context)
"""
def edit_committee(request, committee_name):
    committee = get_object_or_404(Committee, name=committee_name)
    if request.method == 'POST':  # Post form
        form = CommitteeEditForm(request.POST)
        if form.is_valid():

            committee.header = form.cleaned_data['header']
            committee.one_liner = form.cleaned_data['one_liner']
            committee.description = form.cleaned_data['description']
            image_raw = form.cleaned_data['image']
            print(">", image_raw)
            #image_raw = "1"
            try:
                img_id = int(image_raw)
                committee.image = Image.objects.get(id=img_id)
            except (TypeError, ValueError, Image.DoesNotExist):
                committee.image = None

            committee.save()
            #log_changes.change(request, committee)

            return HttpResponseRedirect('/committees')
    else:  # Request form
        try:
            thumb_id = committee.image.id
        except AttributeError:
            thumb_id = 0

        # Set values for edit-form
        form = CommitteeEditForm(initial={
            'header': committee.header,
            'one_liner': committee.one_liner,
            'description': committee.description,
            'image': thumb_id,
        })
    context = {
        'form': form,
    }

    return render(request, 'committees/edit_committee.html', context)
