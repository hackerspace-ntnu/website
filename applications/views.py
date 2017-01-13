from django.shortcuts import render
from django.core.urlresolvers import reverse
from applications.forms import ApplicationForm, ProjectApplicationForm
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import json


# Application page
def application_form(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Søknaden din er mottatt, du vil snart høre fra oss")
        else:
            return JsonResponse(json.dumps(form.errors), status=400, safe=False)
    else:
        # Set the initial choices of the dropdowns
        form = ApplicationForm(initial={
            'group_choice': 'Velg en gruppe',
            'year': 'Velg et årstrinn',
        })

    context = {
        'form': form
    }

    return render(request, 'application_form.html', context)

# Project group specific application page
def project_application_form(request):
    if request.method == 'POST':
        form = ProjectApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return JsonResponse(json.dumps(form.errors), status=400, safe=False)

    form = ProjectApplicationForm()

    context = {
        'form': form
    }

    return render(request, 'project_application_form.html', context)


def application_sent(request):
    return render(request, 'application_sent.html')
