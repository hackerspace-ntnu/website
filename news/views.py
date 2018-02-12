from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import formats
from django.utils import timezone
from datetime import datetime, timedelta
from . import log_changes
from .forms import EventEditForm, ArticleEditForm, UploadForm, EventRegistrationForm, AttendeeForm
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
        'user': request.user,
    }

    if requested_event.internal and not groups.has_group(request.user, 'member'):
        return HttpResponseRedirect('/')

    context['registration_visible'] = False
    if request.user.is_authenticated():
        now = timezone.now()

    if request.user.is_authenticated():
        context['registered'], context['registration_visible'] = requested_event.registration_button_status(request.user)
        context['userstatus'] = requested_event.userstatus(request.user)
    else:
        context['registered'] = False
        context['registration_visible'] = False
        context['userstatus'] = 'Ikke pålogget'

    return render(request, 'event.html', context)


def all_news(request):
    if groups.has_group(request.user, 'member'):
        article_list = list(Article.objects.order_by('-pub_date'))
    else:
        article_list = list(Article.objects.filter(internal=False).order_by('-pub_date'))

    context = {
        'news_list': article_list,
    }

    return render(request, 'news.html', context)


def all_events(request):
    if groups.has_group(request.user, 'member'):
        event_list = list(Event.objects.order_by('-time_start'))
        old_events = list(Event.objects.filter(time_start__lte=datetime.now()).order_by('-time_start'))
        new_events = list(Event.objects.filter(time_start__gte=datetime.now()).order_by('-time_start'))
    else:
        event_list = list(Event.objects.filter(internal=False).order_by('-time_start'))
        old_events = list(Event.objects.filter(internal=False, time_start__lte=datetime.now()).order_by('-time_start'))
        new_events = list(Event.objects.filter(internal=False, time_start__gte=datetime.now()).order_by('-time_start'))


    context = {
        'event_list': event_list,
        'old_events': old_events,
        'new_events': new_events,
        'time_now': datetime.now(),
    }

    return render(request, 'events.html', context)


def article(request, article_id):
    article_id = get_id_or_404(article_id)
    article = get_object_or_404(Article, pk=article_id)
    context = {
        'article': article,
    }

    if article.internal and not groups.has_group(request.user, 'member'):
        return HttpResponseRedirect('/')

    return render(request, 'article.html', context)


def edit_event(request, event_id):
    event_id = get_id_or_404(event_id)
    if request.method == 'POST':  # Post form
        form = EventEditForm(request.POST)
        if form.is_valid():

            # Create new event (ID = 0) or update existing event (ID != 0)
            if event_id:
                event = get_object_or_404(Event, pk=event_id)
            else:
                event = Event()

            for attr in form.cleaned_data:
                setattr(event, attr, form.cleaned_data[attr])


            event.save()

            log_changes.change(request, event)

            return HttpResponseRedirect('/events/' + str(event.id) + '/')
    else:
        if event_id:
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
                'internal': event.internal,
                'place': event.place,
                'place_href': event.place_href,
                'time_start': datetime.strftime(event.time_start, '%H:%M'),
                'time_end': datetime.strftime(event.time_end, '%H:%M'),
                'date': datetime.strftime(event.time_start, '%d %B, %Y'),
                'external_registration': event.external_registration,
                'deregistration_end_date': datetime.strftime(event.deregistration_end, '%d %B, %Y'),
                'deregistration_end_time': datetime.strftime(event.deregistration_end, '%H:%M'),
                'registration_start_date': datetime.strftime(event.registration_start, '%d %B, %Y'),
                'registration_start_time': datetime.strftime(event.registration_start, '%H:%M'),
            })
        else:
            # No event to edit, set data to default
            # Set initial values
            today = datetime.strftime(timezone.now(), '%d %B, %Y')
            form = EventEditForm(initial={
                'time_start': '00:00',
                'time_end': '00:00',
                'date': today,
                'registration_start_time': '00:00',
                'registration_start_date': today,
                'deregistration_end_time': '00:00',
                'deregistration_end_date': today,
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
            article.internal = form.cleaned_data['internal']
            try:
                thumb_id = int(thumbnail_raw)
                article.thumbnail = Image.objects.get(id=thumb_id)
            except (TypeError, ValueError, Image.DoesNotExist):
                article.thumbnail = None
            article.save()
            log_changes.change(request, article)

            return HttpResponseRedirect('/news/' + str(article.id) + '/')
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
                'internal': article.internal,
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

    return HttpResponseRedirect('/news/all')


def delete_event(request, event_id):
    event_id = get_id_or_404(event_id)
    if groups.has_group(request.user, 'member'):
        event = get_object_or_404(Event, pk=event_id)
        event.delete()

    return HttpResponseRedirect('/news/all')


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
    now = timezone.now()
    try:
        er = EventRegistration.objects.get(user=request.user, event=event_object)
        if event_object.deregistration_end > now:
            er.delete()
    except EventRegistration.DoesNotExist:
        if now > event_object.registration_start and event_object.time_end > now:
            EventRegistration.objects.create(event=event_object, user=request.user).save()

    return HttpResponseRedirect("/events/%i" % event_object.id)


def event_attendees(request, event_id):
    if request.method == 'POST':
        try:
            user_string = request.POST['name']
            username = user_string.split("-")[-1].strip()
            user = User.objects.get(username=username)
            event = Event.objects.get(pk=event_id)
            er = EventRegistration.objects.get(event=event, user=user)
            name = er.name() if er.name().strip() != '' else username

            if not er.attended:
                er.attended = True
                er.save()
                message = name + ' er nå registrert'
            else:
                message = name + ' er allerede registrert'

            return JsonResponse({'success': True, 'message': message, 'username': username}, safe=False)

        except IndexError:
            return JsonResponse({'success': False, 'message': 'Fant ikke bruker'}, safe=False)
    else:
        event_object = get_object_or_404(Event, pk=get_id_or_404(event_id))

        form = AttendeeForm()

        context = {
            'id': event_id,
            'form': form,
            'event': event_object,
            'users': EventRegistration.objects.filter(event=event_object),
            'attending_usernames': event_object.attending_usernames(),
        }

        return render(request, 'event_attendees.html', context)


def get_id_or_404(object_id):
    object_id = int(object_id)
    # Raise 404 if ID too large for SQLite (2^63-1) or negative
    if object_id > 9223372036854775807 or object_id < 0:
        raise Http404
    return object_id
