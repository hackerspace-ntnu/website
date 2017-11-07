from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .forms import EditCommittees, EditDescription
from .models import Committee, Member


def index(request):
    # Fetch all members, who belong to a committee (Member -> Committee)
    # Group all these members by the committee type
    committees = Committee.objects.prefetch_related('members')

    context = {
        'committees': committees,
    }

    return render(request, 'committees/list_committees.html', context)


def edit(request):
    form = EditCommittees(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            committee = form.cleaned_data.get('committee')
            position = form.cleaned_data.get('position')
            new_user = form.cleaned_data.get('user')
            try:
                current_member = Member.objects.get(committee=committee,
                                                    position=position)
            except ObjectDoesNotExist:
                current_member = None
            if current_member is not None:
                current_member.delete()
            new_member = Member(committee=committee,
                                position=position,
                                user=new_user)
            new_member.save()
            messages.add_message(request, messages.SUCCESS, 'Brukeren er lagt til i vervet og tidligere bruker er slettet!',
                                 extra_tags='Flott!',
                                )
    context = {
        'form': form,
    }
    return render(request, 'committees/edit.html', context)


def view_committee(request, slug):
    committee = get_object_or_404(Committee, slug=slug)
    members = Member.objects.filter(committee=committee)
    context = {
        'committee': committee,
        'members': members
    }
    return render(request, 'committees/view_committee.html', context)


def edit_description(request, slug):
    committee = get_object_or_404(Committee, slug=slug)
    form = EditDescription(request.POST or None, instance=committee)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.add_message(request, messages.SUCCESS, '{} har blitt endret!'.format(committee.title), extra_tags='Supert')
            return HttpResponseRedirect(committee.get_absolute_url())
    context = {
        'committee': committee,
        'form': form,
    }
    return render(request, 'committees/edit_description.html', context)


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return User.objects.none()

        qs = User.objects.all()

        if self.q:
            qs = qs.filter(username__icontains=self.q)

        return qs
