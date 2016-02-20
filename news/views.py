from django.shortcuts import render

from .models import Event, Article, Thumbnail


def events(request):
    event_list = Event.objects.order_by('-date')
    thumbnail_list = Thumbnail.objects.all()
    context = {
        'event_list': event_list,
        'thumbnail_list': thumbnail_list,
    }

    return render(request, 'events.html', context)


def event(request, event_id):
    event = Event.objects.get(pk=event_id)
    context = {
        'event': event,
    }

    return render(request, 'event.html', context)


def articles(request):
    article_list = Article.objects.order_by('-pub_date')
    thumbnail_list = Thumbnail.objects.all()
    context = {
        'article_list': article_list,
        'thumbnail_list': thumbnail_list,
    }

    return render(request, 'articles.html', context)


def article(request, article_id):
    article = Article.objects.get(pk=article_id)
    context = {
        'article': article,
    }

    return render(request, 'article.html', context)
