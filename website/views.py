from django.shortcuts import render
from news.models import Article, Event
from authentication.forms import LoginForm


def index(request):
    event_list = Event.objects.order_by('-time_start')[:3]
    article_list = Article.objects.order_by('-pub_date')[:3]
    form = LoginForm()
    context = {
        'article_list': article_list,
        'event_list': event_list,
        'form': form,
    }

    return render(request, 'index.html', context)
