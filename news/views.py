from django.shortcuts import render

from .models import Event, Article, Image, Thumbnail


def events(request):
    event_list = Event.objects.order_by('-event_date')
    event_thumbnail_list = Thumbnail.objects.all()
    context = {
        'event_list': event_list,
        'event_thumbnail_list': event_thumbnail_list
    }

    return render(request, 'events.html', context)


def event(request, event_id):
    requested_event = Event.objects.get(pk=event_id)
    try:
        image_list = Image.objects.filter(event_id=event_id)
    except Image.DoesNotExist:
        image_list = None
    if image_list:
        return render(request, 'event.html', {
            'event': requested_event,
            'image_list': image_list
        })
    else:
        return render(request, 'event.html', {
            'event': requested_event
        })


def articles(request):
    article_list = Article.objects.order_by('-pub_date')
    thumbnail_list = Thumbnail.objects.all()
    context = {
        'article_list': article_list,
        'thumbnail_list': thumbnail_list
    }

    return render(request, 'articles.html', context)


def article(request, article_id):
    requested_article = Article.objects.get(pk=article_id)
    try:
        image_list = Image.objects.filter(article_id=article_id)
    except Image.DoesNotExist:
        image_list = None
    if image_list:
        return render(request, 'article.html', {
            'article': requested_article,
            'image_list': image_list
        })
    else:
        return render(request, 'article.html', {
            'article': requested_article
        })
