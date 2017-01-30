from django.shortcuts import render
from django.core.urlresolvers import reverse
from applications.forms import ApplicationForm, ProjectApplicationForm
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from datetime import datetime
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
            send_mail(
                'Hackerspace NTNU takker for interessen :)',
                """Hei og takk for at du er interessert i å søke prosjektgruppa til Hackerspace NTNU! Du får du en epost med link til søknadsskjemaet når det åpner, og kan søke stilling i enten Escape-rom gruppa eller VR-gruppa.

Har du spørsmål eller vil du vite mer om oss eller stillingene? Besøk oss gjerne på Slack:
https://hackerspace-ntnu.slack.com/messages/opptak/

Med vennlig hilsen oss i prosjektgruppa ved Hackerspace NTNU.

https://hackerspace-ntnu.no/
https://www.facebook.com/hackerspacentnu/?fref=ts
""",
                'Hackerspace NTNU',
                [form.cleaned_data['email']],
                fail_silently=False,
            )
            return application_sent(request)
        else:
            return JsonResponse(json.dumps(form.errors), status=400, safe=False)


    form = ProjectApplicationForm()

    context = {
        'form': form
    }
    return render(request, 'project_application_form.html', context)


def application_sent(request):
    return render(request, 'application_sent.html')


def no_application(request):
    return render(request, 'no_application.html', {})
