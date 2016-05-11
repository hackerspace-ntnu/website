from django.shortcuts import render
from applications.forms import ApplicationForm


def application_form(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)

    else:
        form = ApplicationForm()

    context = {
        'form': form
    }

    return render(request, 'application_form.html', context)

