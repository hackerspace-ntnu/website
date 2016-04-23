from django.shortcuts import render
from news.models import Article, Event
from door.models import DoorStatus
from authentication.forms import LoginForm
from django_user_agents.utils import get_user_agent
from local_settings import DEBUG


def index(request):
    event_list = Event.objects.order_by('-time_start')[:3]
    article_list = Article.objects.order_by('-pub_date')[:3]
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


def test404(request):
    return render(request, '404.html')

def test500(request):
    return render(request, '500.html')
