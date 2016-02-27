from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Event, Article, Thumbnail, Upload
from .forms import EventEditForm, ArticleEditForm, UploadForm
from . import log_changes
from django import forms
from django.utils import formats
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils import timezone


def events(request):
    event_list = Event.objects.order_by('-time_start')
    thumbnail_list = Thumbnail.objects.all()
    context = {
        'event_list': event_list,
        'thumbnail_list': thumbnail_list,
    }

    return render(request, 'events.html', context)


def event(request, event_id):
    requested_event = Event.objects.get(pk=event_id)
    form = EventEditForm(initial={
        'event_id': event_id,
        'ingress_content': requested_event.ingress_content,
        'main_content': requested_event.main_content,
        'place': requested_event.place,
        'place_href': requested_event.place_href,
        'time_start': formats.date_format(requested_event.time_start, 'H:i'),
        'time_end': formats.date_format(requested_event.time_end, 'H:i'),
        'date': formats.date_format(requested_event.time_start, 'd/m/Y'),
    })
    context = {
        'event': requested_event,
        'form': form
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
    requested_article = Article.objects.get(pk=article_id)
    form = ArticleEditForm(initial={
        'article_id': article_id,
        'ingress_content': requested_article.ingress_content,
        'main_content': requested_article.main_content
    })
    form.fields['article_id'].widget = forms.HiddenInput()
    context = {
        'article': requested_article,
        'form': form,
    }

    return render(request, 'article.html', context)


def edit_event(request):
    if request.method == 'POST':
        form = EventEditForm(request.POST)
        if form.is_valid():
            event_id = form.cleaned_data['event_id']
            event = Event.objects.get(pk=event_id)
            event.ingress_content = form.cleaned_data['ingress_content']
            event.main_content = form.cleaned_data['main_content']
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
            return HttpResponseRedirect('/news/event/'+str(event_id)+'/')
    else:
        form = EventEditForm()

    return render(request, 'edit_event.html', {'form': form})


def edit_article(request):
    if request.method == 'POST':
        form = ArticleEditForm(request.POST)
        if form.is_valid():
            article_id = form.cleaned_data['article_id']
            article = Article.objects.get(pk=article_id)
            article.ingress_content = form.cleaned_data['ingress_content']
            article.main_content = form.cleaned_data['main_content']
            article.save()
            log_changes.change(request, article)

            return HttpResponseRedirect('/news/article/'+str(article_id)+'/')
    else:
        form = ArticleEditForm()

    return render(request, 'edit_article.html', {'form': form})


def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            file = request.FILES['file']
            number = 0

            for element in Upload.objects.order_by('-time'):
                if title == element.title:
                    number = element.number + 1
                    break

            ext = file.name.split(".")[-1:][0]
            file.name="/upload/"+title+"_"+str(number)+"."+ext
            instance = Upload(file=file, title=title, time=timezone.now(), number=number)
            instance.save()
            return HttpResponseRedirect('/news/upload-done')
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})


def upload_done(request):
    return render(request, 'upload_done.html')
