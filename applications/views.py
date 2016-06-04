from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from applications.forms import ApplicationForm
from applications.models import Application


# Application page
def application_form(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = Application.objects.create(name=form.cleaned_data['name'],
                                                     email=form.cleaned_data['email'],
                                                     phone=form.cleaned_data['phone'],
                                                     study=form.cleaned_data['study'],
                                                     group_choice=form.cleaned_data['group_choice'],
                                                     year=form.cleaned_data['year'],
                                                     knowledge_of_hs=form.cleaned_data['knowledge_of_hs'],
                                                     about=form.cleaned_data['about'],
                                                     application_text=form.cleaned_data['application_text'])

            application.save()
            return HttpResponseRedirect(reverse('application_sent'))

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


def application_sent(request):
    return render(request, 'application_sent.html')
