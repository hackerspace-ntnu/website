from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import JsonResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from .forms import CommitteeCreateForm, CommitteeEditForm
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
            raise Http404()

        # Id to all subcommittees
        sub_ids = committee.subcommittees.values_list('id', flat=True)

        # Id to all members of subcommittees
        subgroup_members = []
        for sub_id in sub_ids:
            sub_members_ids = Committee.objects.get(pk=sub_id).user_set.all().values_list('id', flat=True)
            subgroup_members.extend(sub_members_ids)

        # Get members of committee who isn't in any subcommittee.
        users = committee.user_set.exclude(id__in=subgroup_members).order_by('first_name')

        context = {
            'can_edit': is_committee_admin(request.user, committee),
            'committee': committee,
            'form': CommitteeCreateForm(),
            'users': users,
        }
        return render(request, 'committees/view_committee.html', context)

    @staticmethod
    def post(request, slug):
        """ View for creating subcommittees. """
        committee = Committee.objects.get(slug=slug)
        form = CommitteeCreateForm(request.POST, parent_committee=committee)

        if form.is_valid():
            name = form.cleaned_data['name']
            # Create new slug based on parents slug and new name.
            sub_slug = committee.slug + "-" + name
            Committee.objects.create(name=name, slug=sub_slug, parent=committee)
            return JsonResponse({'redirect_url': reverse('committees:edit_committee', args=(sub_slug,))})
        else:
            return JsonResponse({'errors': form.errors})


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

        if user not in committee.user_set.all():
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


def edit_committee(request, slug):
    # TODO for endring av parent, må slug endres til at den stemmer med treet.
    committee = get_object_or_404(Committee, slug=slug)

    # Only admins for this committee can edit it.
    if not is_committee_admin(request.user, committee):
        raise Http404()

    if request.method == 'POST':  # Post form
        form = CommitteeEditForm(request.POST)
        if form.is_valid():

            committee.header = form.cleaned_data['header']
            committee.one_liner = form.cleaned_data['one_liner']
            committee.description = form.cleaned_data['description']

            # Setting picture.
            thumb_raw = form.cleaned_data['thumbnail']
            try:
                thumb_id = int(thumb_raw)
                committee.thumbnail = Image.objects.get(id=thumb_id)
            except (TypeError, ValueError, Image.DoesNotExist):
                committee.thumbnail = None

            committee.save()
            return HttpResponseRedirect(reverse('committees:list_all'))

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

    return render(request, 'committees/edit_committee.html', {
        'committee': committee,
        'form': form,
    })
