from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from news.models import Article, Event
from door.models import DoorStatus
from datetime import datetime
from wiki.templatetags import check_user_group as groups


def index(request, number_of_news=3):
    # Sorts the news to show the events nearest in future and then fill in with the newest articles
    can_access_internal = groups.has_group(request.user, 'member')

    event_list = Event.objects.filter(time_end__gte=datetime.now(), internal__lte=can_access_internal).order_by('time_start')
    article_list = Article.objects.filter(internal__lte=can_access_internal).order_by('-pub_date')

    news_list = (list(event_list) + list(article_list))[:number_of_news]

    try:
        door_status = DoorStatus.objects.get(name='hackerspace').status
    except DoorStatus.DoesNotExist:
        door_status = True

    context = {
        'news_list': news_list,
        'door_status': door_status,
    }

    return render(request, 'index.html', context)


def opptak(request):
    return HttpResponseRedirect(reverse('article', args=[7]))


def test(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        raise Exception("Manuell test av 500 - internal server error")
    else:
        raise Http404


def handler404(request):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)


def calendar(request):
    return render(request, 'calendar.html')


def about(request):
    return render(request, 'about.html')
