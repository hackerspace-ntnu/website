from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import formats
from django.utils import timezone
from datetime import datetime, timedelta
from . import log_changes
from .forms import EventEditForm, ArticleEditForm, UploadForm, EventRegistrationForm
from .models import Event, Article, Upload, EventRegistration
from itertools import chain
from wiki.templatetags import check_user_group as groups
from django.contrib.auth.admin import User
from django.contrib.auth.decorators import login_required
from files.models import Image


def event(request, event_id):
    event_id = get_id_or_404(event_id)
    requested_event = get_object_or_404(Event, pk=event_id)
    context = {
        'event': requested_event,
    }

    if request.user.is_authenticated():

        event_reg = EventRegistration.objects.filter(user=request.user, event=requested_event)

        if event_reg:
            context['registered'] = True

    return render(request, 'event.html', context)


def all_news(request):
    article_list = list(Article.objects.order_by('pub_date'))
    event_list = list(Event.objects.order_by('time_start'))
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
    article_id = get_id_or_404(article_id)
    article = get_object_or_404(Article, pk=article_id)
    context = {
        'article': article,
    }

    return render(request, 'article.html', context)


def edit_event(request, event_id):
    event_id = get_id_or_404(event_id)
    if request.method == 'POST':  # Post form
        form = EventEditForm(request.POST)
        if form.is_valid():
            # Create new event (ID = 0) or update existing event (ID != 0)
            if event_id == 0:
                event = Event(time_start=timezone.now(), time_end=timezone.now())
            else:
                event = get_object_or_404(Event, pk=event_id)
            event.title = form.cleaned_data['title']
            event.ingress_content = form.cleaned_data['ingress_content']
            event.main_content = form.cleaned_data['main_content']
            event.registration = form.cleaned_data['registration']
            event.max_limit = form.cleaned_data['max_limit']
            thumbnail_raw = form.cleaned_data['thumbnail']
            try:
                thumb_id = int(thumbnail_raw)
                event.thumbnail = Image.objects.get(id=thumb_id)
            except (TypeError, Image.DoesNotExist):
                event.thumbnail = None
            event.place = form.cleaned_data['place']
            event.place_href = form.cleaned_data['place_href']
            # Create date from string input
            event.date = datetime.strptime(form.cleaned_data['date'], '%d %B, %Y').date()
            # Create datetime from string input
            event.time_start = datetime.strptime(form.cleaned_data['date'] + ' ' + form.cleaned_data['time_start'],
                                                 '%d %B, %Y %H:%M')
            event.time_end = datetime.strptime(form.cleaned_data['date'] + ' ' + form.cleaned_data['time_end'],
                                               '%d %B, %Y %H:%M')
            event.save()
            log_changes.change(request, event)
            return HttpResponseRedirect('/news/event/' + str(event.id) + '/')
    else:  # Request form
        # Create new event if ID is 0
        if int(event_id) == 0:
            # Set initial values
            form = EventEditForm(initial={
                'time_start': '00:00',
                'time_end': '00:00',
                'date': formats.date_format(timezone.now(), 'd F, Y'),
            })
        else:
            event = get_object_or_404(Event, pk=event_id)

            try:
                thumb_id = event.thumbnail.id
            except AttributeError:
                thumb_id = 0

            # Set values for edit-form
            form = EventEditForm(initial={
                'title': event.title,
                'ingress_content': event.ingress_content,
                'main_content': event.main_content,
                'thumbnail': thumb_id,
                'max_limit': event.max_limit,
                'registration': event.registration,
                'place': event.place,
                'place_href': event.place_href,
                'time_start': formats.date_format(event.time_start, 'H:i'),
                'time_end': formats.date_format(event.time_end, 'H:i'),
                'date': datetime.strftime(event.time_start, '%-d %B, %Y'),
            })

    context = {
        'form': form,
    }

    return render(request, 'edit_event.html', context)


def edit_article(request, article_id):
    article_id = get_id_or_404(article_id)
    if request.method == 'POST':  # Post form
        form = ArticleEditForm(request.POST)
        if form.is_valid():
            if article_id == 0:
                article = Article()
            else:
                article = get_object_or_404(Article, pk=article_id)
            article.title = form.cleaned_data['title']
            article.ingress_content = form.cleaned_data['ingress_content']
            article.main_content = form.cleaned_data['main_content']
            thumbnail_raw = form.cleaned_data['thumbnail']
            try:
                thumb_id = int(thumbnail_raw)
                article.thumbnail = Image.objects.get(id=thumb_id)
            except (TypeError, Image.DoesNotExist):
                article.thumbnail = None
            article.save()
            log_changes.change(request, article)

            return HttpResponseRedirect('/news/article/' + str(article.id) + '/')
    else:  # Request form
        if article_id == 0:
            form = ArticleEditForm()
        else:
            article = get_object_or_404(Article, pk=article_id)

            try:
                thumb_id = article.thumbnail.id
            except AttributeError:
                thumb_id = 0

            # Set values for edit-form
            form = ArticleEditForm(initial={
                'title': article.title,
                'ingress_content': article.ingress_content,
                'main_content': article.main_content,
                'thumbnail': thumb_id,
            })
    context = {
        'form': form,
    }

    return render(request, 'edit_article.html', context)


def delete_article(request, article_id):
    article_id = get_id_or_404(article_id)
    if groups.has_group(request.user, 'member'):
        article = get_object_or_404(Article, pk=article_id)
        article.delete()

    return HttpResponseRedirect('/')


def delete_event(request, event_id):
    event_id = get_id_or_404(event_id)
    if groups.has_group(request.user, 'member'):
        event = get_object_or_404(Event, pk=event_id)
        event.delete()

    return HttpResponseRedirect('/')


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
        form = UploadForm(initial={
            'title': '',
            'file': '',
        })

    context = {
        'form': form,
    }
    return render(request, 'upload.html', context)


def upload_done(request):
    return render(request, 'upload_done.html')


@login_required
def register_on_event(request, event_id):

    event_object = get_object_or_404(Event, pk=get_id_or_404(event_id))
    event_reg = EventRegistration.objects.filter(user=request.user, event=event_object)
    if event_reg:
        for ev in event_reg:
            ev.delete()
            event_object.registered_users -= 1
    else:
        if event_object.registered_users < event_object.max_limit:
            EventRegistration.objects.create(event=event_object, user=request.user).save()
            event_object.registered_users += 1

    event_object.save()
    return HttpResponseRedirect("/news/event/" + str(event_object.id))


def get_id_or_404(object_id):
    object_id = int(object_id)
    # Raise 404 if ID too large for SQLite (2^63-1) or negative
    if object_id > 9223372036854775807 or object_id < 0:
        raise Http404
    return object_id
