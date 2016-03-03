from django.shortcuts import render
from news.models import Article, Event
from door.models import DoorStatus
from authentication.forms import LoginForm


def index(request):
    event_list = Event.objects.order_by('-time_start')[:3]
    article_list = Article.objects.order_by('-pub_date')[:3]
    if DoorStatus.objects.filter(name='hackerspace').count():
        door_status = DoorStatus.objects.get(name='hackerspace').status
    else:
        door_status = True
    form = LoginForm()
    context = {
        'article_list': article_list,
        'event_list': event_list,
        'form': form,
        'door_status': door_status,
    }

    return render(request, 'index.html', context)
