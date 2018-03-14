from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from news.models import Article, Event
from files.models import Image
from door.models import DoorStatus
from datetime import datetime
from wiki.templatetags import check_user_group as groups


def showcase(request):
    context = {

    }
    return render(request, 'website/showcase.html', context)

def virtualreality(request):

    context = {

    }
    return render(request, 'website/vr.html', context)



def index(request):
    # Sorts the news to show the events nearest in future and then fill in with the newest articles
    can_access_internal = groups.has_group(request.user, 'member')

    # First sort, then grab 5 elements, then flip the list ordered by date
    event_list = Event.objects.filter(internal__lte=can_access_internal).order_by('-time_start')[:5:-1]

    # Get five articles
    article_list = Article.objects.filter(internal__lte=can_access_internal).order_by('-pub_date')[:5]

    event_list = list(event_list)
    artile_list = list(article_list)

    try:
        door_status = DoorStatus.objects.get(name='hackerspace').status
    except DoorStatus.DoesNotExist:
        door_status = True


    context = {
        'article_list': article_list,
        'event_list': event_list,
        'door_status': door_status,
    }
    return render(request, 'website/index.html', context)


def opptak(request):
    return HttpResponseRedirect(reverse('article', args=[7]))


def test(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        raise Exception("Manuell test av 500 - internal server error")
    else:
        raise Http404


def handler404(request):
    return render(request, 'website/404.html', status=404)


def handler500(request):
    return render(request, 'website/500.html', status=500)


def calendar(request):
    return render(request, 'website/calendar.html')


def about(request):
    return render(request, 'website/about.html')
