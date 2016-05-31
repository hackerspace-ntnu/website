from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils import formats
from django.utils import timezone
from . import log_changes
from .forms import EventEditForm, ArticleEditForm, UploadForm
from .models import Event, Article, Upload
from itertools import chain


def event(request, event_id):
    requested_event = get_object_or_404(Event, pk=event_id)
    context = {
        'event': requested_event,
    }

    return render(request, 'event.html', context)


def all_news(request):
    article_list = list(Article.objects.order_by('pub_date'))
    event_list = list(Event.objects.order_by('pub_date'))
    news_list = []
    # Create a list mixed with both articles and events sorted after publication date
    for i in range(len(article_list) + len(event_list)):
        if len(article_list) == 0:
            news_list.append(event_list.pop())
            continue
        elif len(event_list) == 0:
            news_list.append(article_list.pop())
            continue
        if article_list[len(article_list) - 1].pub_date > event_list[len(event_list) - 1].time_start:
            news_list.append(article_list.pop())
        else:
            news_list.append(event_list.pop())

    context = {
        'news_list': news_list,
    }

    return render(request, 'all_news.html', context)


def article(request, article_id):
    requested_article = get_object_or_404(Article, pk=article_id)
    context = {
        'article': requested_article,
    }

    return render(request, 'article.html', context)


def edit_event(request, event_id):
    if request.method == 'POST':
        form = EventEditForm(request.POST)
        if form.is_valid():
            event_id = form.cleaned_data['event_id']
            if event_id == 0:
                event = Event(time_start=timezone.now(), time_end=timezone.now())
            else:
                event = get_object_or_404(Event,pk=event_id)
            event.title = form.cleaned_data['title']
            event.ingress_content = form.cleaned_data['ingress_content']
            event.main_content = form.cleaned_data['main_content']
            event.thumbnail = form.cleaned_data['thumbnail']
            event.place = form.cleaned_data['place']
            event.place_href = form.cleaned_data['place_href']
            hour_start = int(form.cleaned_data['time_start'][:2])
            minute_start = int(form.cleaned_data['time_start'][-2:])
            hour_end = int(form.cleaned_data['time_end'][:2])
            minute_end = int(form.cleaned_data['time_end'][-2:])
            day = int(form.cleaned_data['date'][:2])
            month = int(form.cleaned_data['date'][3:5])
            year = int(form.cleaned_data['date'][-4:])
            event.time_start = event.time_start.replace(hour=hour_start, minute=minute_start)
            event.time_start = event.time_start.replace(day=day, month=month, year=year)
            event.time_end = event.time_end.replace(hour=hour_end, minute=minute_end)
            event.time_end = event.time_end.replace(day=day, month=month, year=year)
            event.save()
            log_changes.change(request, event)
            return HttpResponseRedirect('/news/event/' + str(event.id) + '/')
    else:
        if int(event_id) == 0:
            form = EventEditForm(initial={
                'event_id': 0,
                'time_start': '00:00',
                'time_end': '00:00',
                'date': formats.date_format(timezone.now(), 'd/m/Y'),
            })
        else:
            requested_event = Event.objects.get(pk=event_id)
            form = EventEditForm(initial={
                'title': requested_event.title,
                'event_id': event_id,
                'ingress_content': requested_event.ingress_content,
                'main_content': requested_event.main_content,
                'thumbnail': requested_event.thumbnail,
                'place': requested_event.place,
                'place_href': requested_event.place_href,
                'time_start': formats.date_format(requested_event.time_start, 'H:i'),
                'time_end': formats.date_format(requested_event.time_end, 'H:i'),
                'date': formats.date_format(requested_event.time_start, 'd/m/Y'),
            })

    context = {
        'form': form,
        'event_id': event_id,
    }

    return render(request, 'edit_event.html', context)


def edit_article(request, article_id):
    if request.method == 'POST':
        form = ArticleEditForm(request.POST)
        if form.is_valid():
            article_id = form.cleaned_data['article_id']
            if not article_id:
                article = Article()
            else:
                article = get_object_or_404(Article, pk=article_id)
            article.title = form.cleaned_data['title']
            article.ingress_content = form.cleaned_data['ingress_content']
            article.main_content = form.cleaned_data['main_content']
            article.thumbnail = form.cleaned_data['thumbnail']
            article.save()
            log_changes.change(request, article)

            return HttpResponseRedirect('/news/article/' + str(article.id) + '/')
    else:
        if int(article_id) == 0:
            form = ArticleEditForm(initial={
                'article_id': 0,
            })
        else:
            requested_article = Article.objects.get(pk=article_id)
            form = ArticleEditForm(initial={
                'title': requested_article.title,
                'article_id': article_id,
                'ingress_content': requested_article.ingress_content,
                'main_content': requested_article.main_content,
                'thumbnail': requested_article.thumbnail,
            })
    context = {
        'form': form,
        'article_id': article_id,
    }

    return render(request, 'edit_article.html', context)


def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            title = str(form.cleaned_data['title']).replace(" ", "_")
            file = request.FILES['file']
            number = 0

            for element in Upload.objects.order_by('-time'):
                if title == element.title:
                    number = element.number + 1
                    break

            ext = file.name.split(".")[-1:][0]
            file.name = "/upload/" + title + "_" + str(number) + "." + ext
            instance = Upload(file=file, title=title, time=timezone.now(), number=number)
            instance.save()
            return HttpResponseRedirect('/news/upload-done')
    else:
        form = UploadForm()

    context = {
        'form': form,
    }
    return render(request, 'upload.html', context)


def upload_done(request):
    return render(request, 'upload_done.html')
