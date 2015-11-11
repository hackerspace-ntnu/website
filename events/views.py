from django.shortcuts import render

from events.models import Event, Image, Thumbnail


def index(request):
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
