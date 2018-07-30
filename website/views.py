from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from news.models import Article, Event
from door.models import DoorStatus
from userprofile.models import Profile
from authentication.templatetags import check_user_group as groups


def showcase(request):
    return render(request, 'website/showcase.html')


def tos(request):
    return render(request, 'website/tos.html')

def tosreturn(request):
    return render(request, 'website/tos-returningls.html')

def tosaccept(request):
    profileobj = get_object_or_404(Profile, pk=request.user.profile.id)
    if(profileobj != None):
        profileobj.tos_accepted = True
        profileobj.save()

    return HttpResponseRedirect('/')


def virtualreality(request):
    return render(request, 'website/vr.html')


def index(request):
    can_access_internal = groups.has_group(request.user, 'member')

    # First sort, then grab 5 elements, then flip the list ordered by date
    event_list = Event.objects.filter(
        internal__lte=can_access_internal).order_by('-time_start')[:5:-1]

    # Get five articles
    article_list = Article.objects.filter(
        internal__lte=can_access_internal).order_by('-pub_date')[:5]

    try:
        door_status = DoorStatus.objects.get(name='hackerspace').status
    except DoorStatus.DoesNotExist:
        door_status = True

    context = {
        'article_list': article_list,
        'event_list': event_list,
        'door_status': door_status,
    }
    return render(request, 'website/index.html', context)


def opptak(request):
    return HttpResponseRedirect(reverse('article', args=[7]))


def test(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        raise Exception("Manuell test av 500 - internal server error")
    else:
        raise Http404


def handler404(request):
    return render(request, 'website/404.html', status=404)


def handler500(request):
    return render(request, 'website/500.html', status=500)


def calendar(request):
    return render(request, 'website/calendar.html')


def about(request):
    return render(request, 'website/about.html')
