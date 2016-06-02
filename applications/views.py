from django.shortcuts import render
from applications.forms import ApplicationForm


def application_form(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)

    else:
        form = ApplicationForm(initial={
            'group_choice': 'Velg en gruppe',
            'year': 'Velg et årstrinn',
        })

    context = {
        'form': form
    }

    return render(request, 'application_form.html', context)
