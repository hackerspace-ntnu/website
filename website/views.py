from django.shortcuts import render
from news.models import Article, Event
from door.models import DoorStatus
from datetime import datetime
from itertools import chain


def index(request):

    number_of_news = 3

    # Sorts the news to show the events nearest in future and then fill in with the newest articles
    event_list = Event.objects.filter(time_end__gte=datetime.now())[0:number_of_news:-1]
    article_list = Article.objects.order_by('-pub_date')[0:number_of_news - len(event_list)]
    news_list = list(chain(event_list, article_list))

    try:
        door_status = DoorStatus.objects.get(name='hackerspace').status
    except DoorStatus.DoesNotExist:
        door_status = True
    context = {
        'news_list': news_list,
        'door_status': door_status,
    }

    return render(request, 'index.html', context)


def test404(request):
    return render(request, '404.html')
