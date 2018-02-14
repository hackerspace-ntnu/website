from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
import json

from .forms import CommitteeEditForm
from .models import Committee
from .templatetags.access import is_committee_admin
from files.models import Image


def index(request):
    committees = Committee.objects.prefetch_related('user_set')

    context = {
        'committees': committees,
    }

    return render(request, 'committees/list_committees.html', context)


class ViewCommittee(View):
    @staticmethod
    def get(request, slug):
        committee = get_object_or_404(Committee, slug=slug)

        if not (committee.visible or is_committee_admin(request.user, committee)):
            raise Http404

        # positions = Position.objects.filter(pos_in_committee=committee)
        # pos_names = [p.usr.username for p in positions]

        # users = [user for user in committee.user_set.all() if user.username not in pos_names]
        # users = filter(lambda user: user.username not in pos_names, committee.user_set.all())
        users = list(committee.user_set.all())
        users.sort(key=lambda user: user.first_name)
        context = {
            'committee': committee,
            'can_edit': is_committee_admin(request.user, committee),
            'users': users,
        }
        return render(request, 'committees/view_committee.html', context)

    @staticmethod
    def put(request, slug):
        """ Method to remove user from team.
            DELETE workshop:setup_workshop <code> data={"maker_id": "<id>"}
        """
        committee = Committee.objects.get(slug=slug)
        group_name = request.body.decode()[5:]
        sub_slug = committee.slug + "-" + group_name
        # TODO nekt å opprette subcommittee hvis denne har en som eksisterer fra før, siden slug må være unik
        Committee.objects.create(name=group_name, slug=sub_slug, parent=committee)
        return JsonResponse({'success': 1})


def edit_members(request, slug):
    committee = get_object_or_404(Committee, slug=slug)
    if is_committee_admin(request.user, committee):
        if request.method == 'POST':
            if request.POST['action'] == 'add':
                json = add_member(request, slug)
            elif request.POST['action'] == 'delete':
                json = delete_member(request, slug)
            return json
        else:
            print(slug)
            committee = get_object_or_404(Committee, slug=slug)

            context = {
                'committee': committee,
                'usernames': [user.username for user in committee.user_set.all()],
                'all_users': User.objects.all(),
            }

            return render(request, 'committees/edit_members.html', context)
    else:
        return HttpResponseForbidden()


def add_member(request, slug):
    try:
        user_string = request.POST['name']
        username = user_string.split("-")[-1].strip()
        user = User.objects.get(username=username)
        committee = Committee.objects.get(slug=slug)
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


def delete_member(request, slug):
    try:
        username = request.POST['name']
        print(username)
        user = User.objects.get(username=username)
        committee = Committee.objects.get(slug=slug)
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


def edit_committee(request, slug):
    committee = get_object_or_404(Committee, slug=slug)
    if request.method == 'POST':  # Post form
        form = CommitteeEditForm(request.POST)
        if form.is_valid():

            committee.header = form.cleaned_data['header']
            committee.one_liner = form.cleaned_data['one_liner']
            committee.description = form.cleaned_data['description']
            thumb_raw = form.cleaned_data['thumbnail']

            try:
                thumb_id = int(thumb_raw)
                committee.thumbnail = Image.objects.get(id=thumb_id)
            except (TypeError, ValueError, Image.DoesNotExist):
                committee.thumbnail = None

            committee.save()
            #log_changes.change(request, committee)

            return HttpResponseRedirect('/committees')
    else:  # Request form
        try:
            thumb_id = committee.thumbnail.id
        except AttributeError:
            thumb_id = 0

        # Set values for edit-form
        form = CommitteeEditForm(initial={
            'header': committee.header,
            'one_liner': committee.one_liner,
            'description': committee.description,
            'thumbnail': thumb_id,
        })
    context = {
        'form': form,
    }
    return render(request, 'committees/edit_committee.html', context)
