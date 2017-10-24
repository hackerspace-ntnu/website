from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .forms import EditCommittees, EditDescription
from .models import Committee


def index(request):
    # Fetch all members, who belong to a committee (Member -> Committee)
    # Group all these members by the committee type
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
