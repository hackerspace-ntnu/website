from django.shortcuts import render
from news.models import Article, Event
from door.models import DoorStatus
from authentication.forms import LoginForm
from django_user_agents.utils import get_user_agent
from local_settings import DEBUG
from datetime import datetime


def index(request):

    number_of_news = 4

    # Sorts the news to show the events nearest in future and then fill in with the newest articles
    event_list = Event.objects.filter(time_start__gte=datetime.now())[0:number_of_news:-1]
    article_list = Article.objects.order_by('-pub_date')[0:number_of_news - len(event_list)]

    try:
        door_status = DoorStatus.objects.get(name='hackerspace').status
    except DoorStatus.DoesNotExist:
        door_status = True
    form = LoginForm()
    user_agent = get_user_agent(request)
    context = {
        'article_list': article_list,
        'event_list': event_list,
        'form': form,
        'door_status': door_status,
        'mobile': user_agent.is_mobile,
    }

    return render(request, 'index.html', context)


def info_screen(request):
    return render(request, 'info_screen.html')


def test404(request):
    return render(request, '404.html')
