from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .forms import EditCommittees, EditDescription
from .models import Committee

@permission_required('committees.view_committees')
def index(request):
    committees = Committee.objects.prefetch_related('user_set')

    context = {
        'committees': committees,
    }

    return render(request, 'committees/list_committees.html', context)

@permission_required('committees.view_committees')
def view_committee(request, name):
    committee = get_object_or_404(Committee, name=name)
    #members = Member.objects.filter(committee=committee)
    context = {
        'committee': committee,
        'members': committee.user_set.all()
    }
    return render(request, 'committees/view_committee.html', context)

@permission_required('committees.edit_committees')
def edit_members(request, name):
    if request.method == 'POST':
        try:
            user_string = request.POST['name']
            username = user_string.split("-")[-1].strip()
            user = User.objects.get(username=username)
            event = Event.objects.get(pk=event_id)
            er = EventRegistration.objects.get(event=event, user=user)
            name = er.name() if er.name().strip() != '' else username

            if not er.attended:
                er.attended = True
                er.save()
                message = name + ' er nå registrert'
            else:
                message = name + ' er allerede registrert'

            return JsonResponse({'success': True, 'message': message, 'username': username}, safe=False)

        except IndexError:
            return JsonResponse({'success': False, 'message': 'Fant ikke bruker'}, safe=False)
    else:
        committee = get_object_or_404(Committee, name=name)
        context = {
            'committee': committee,
            'members': committee.user_set.all(),
            'all_users': User.objects.all(),
        }

        return render(request, 'committees/edit_members.html', context)
