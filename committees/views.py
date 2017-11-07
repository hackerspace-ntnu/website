from dal import autocomplete
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

from .forms import EditCommittees, EditDescription
from .models import Committee

def index(request):
    committees = Committee.objects.prefetch_related('user_set')

    context = {
        'committees': committees,
    }

    return render(request, 'committees/list_committees.html', context)

def view_committee(request, name):
    committee = get_object_or_404(Committee, name=name)
    #members = Member.objects.filter(committee=committee)
    context = {
        'committee': committee,
        'members': committee.user_set.all()
    }
    return render(request, 'committees/view_committee.html', context)

def edit_check(user, c_name):
    committee = get_object_or_404(Committee, name=c_name)
    return user.has_perm('edit_committees') or user in committee.admins.all()

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
