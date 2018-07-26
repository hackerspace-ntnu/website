from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import TemplateView, DetailView, ListView, FormView, UpdateView, CreateView, DeleteView
from datetime import datetime
from .forms import EventForm
from .models import Event, Article, EventRegistration
from authentication.templatetags import check_user_group as groups
from django.contrib.auth.decorators import login_required

class EventView(DetailView):
    model = Event
    template_name = "news/event.html"

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().internal and not groups.has_group(self.request.user, 'member'):
            return redirect("/")

        return super(EventView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['userstatus'] = "ikke pålogget"

        if self.request.user.is_authenticated:
            context_data['registered'] = self.object.is_registered(self.request.user) or \
                                         self.object.is_waiting(self.request.user)
            context_data['registration_visible'] = self.object.can_edit_registration_status(
                self.request.user)
            context_data['userstatus'] = self.object.userstatus(self.request.user)

        return context_data

class EventListView(ListView):
    template_name = "news/events.html"

    def get_queryset(self):
        if groups.has_group(self.request.user, 'member'):
            return Event.objects.order_by('-time_start')
        else:
            return Event.objects.filter(internal=False).order_by('-time_start')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # Split into two seperate lists
        context_data['old_events'] = self.object_list.filter(time_start__lte=datetime.now()).order_by('-time_start')
        context_data['new_events'] = self.object_list.filter(time_start__gte=datetime.now()).order_by('-time_start')

        return context_data

class ArticleListView(ListView):
    template_name = "news/news.html"

    def get_queryset(self):
        if groups.has_group(self.request.user, 'member'):
            return Article.objects.order_by('-pub_date')
        else:
            return Article.objects.filter(internal=False).order_by('-pub_date')


class ArticleView(DetailView):
    model = Article
    template_name = "news/article.html"

    def dispatch(self, request, *args, **kwargs):
        # Check if user is member if the article field internal is True
        if self.get_object().internal and not groups.has_group(request.user, 'member'):
            return redirect("/")

        return super(ArticleView, self).dispatch(request, *args, **kwargs)


class EventUpdateView(UpdateView):
    model = Event
    template_name = "news/edit_event.html"
    form_class = EventForm
    success_url = "/events/"

    def dispatch(self, request, *args, **kwargs):
        if not groups.has_group(self.request.user, 'member'):
            return redirect("/")

        return super(EventUpdateView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(EventUpdateView, self).get_initial()
        initial['time_start'] = self.object.time_start.date().strftime('%Y-%m-%d')
        initial['time_end'] = self.object.time_end.date().strftime('%Y-%m-%d')
        initial['event_start_time'] = self.object.time_start.time()
        initial['event_end_time'] = self.object.time_end.time()
        initial['registration_start_time'] = self.object.registration_start.time()
        initial['registration_start'] = self.object.registration_start.date().strftime('%Y-%m-%d')
        initial['deregistration_end'] = self.object.deregistration_end.date().strftime('%Y-%m-%d')
        initial['deregistration_end_time'] = self.object.deregistration_end.time()
        return initial


class EventCreateView(CreateView):
    model = Event
    template_name = "news/edit_event.html"
    form_class = EventForm
    success_url = "/events/"

    def dispatch(self, request, *args, **kwargs):
        if not groups.has_group(self.request.user, 'member'):
            return redirect("/")

        return super(EventCreateView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        today = datetime.strftime(timezone.now(), '%Y-%m-%d')

        initial = super(EventCreateView, self).get_initial()
        initial['event_start_time'] = "00:00"
        initial['event_end_time'] = "00:00"
        initial['registration_start_time'] = "00:00"
        initial['deregistration_end_time'] = "00:00"

        initial['time_start'] = today
        initial['time_end'] = today
        initial['registration_start'] = today
        initial['deregistration_end'] = today
        return initial


class ArticleCreateView(CreateView):
    model = Article
    fields = ['title', 'ingress_content', 'main_content', 'thumbnail', 'internal']
    template_name = "news/edit_article.html"
    success_url = "/news/"

    def dispatch(self, request, *args, **kwargs):
        if not groups.has_group(self.request.user, 'member'):
            return redirect("/")
        return super(ArticleCreateView, self).dispatch(request, *args, **kwargs)

class ArticleUpdateView(UpdateView):
    model = Article
    template_name = "news/edit_article.html"
    fields = ['title', 'ingress_content', 'main_content', 'thumbnail', 'internal']
    success_url = "/news/"

    def dispatch(self, request, *args, **kwargs):
        if not groups.has_group(self.request.user, 'member'):
            return redirect("/")

        return super(ArticleUpdateView, self).dispatch(request, *args, **kwargs)

class ArticleDeleteView(DeleteView):
    model = Article
    success_url = "/news/"

    def dispatch(self, request, *args, **kwargs):
        if not groups.has_group(self.request.user, 'member'):
            return redirect("/")

        return super(ArticleDeleteView, self).dispatch(request, *args, **kwargs)

class EventDeleteView(DeleteView):
    model = Event
    success_url = "/events/"

    def dispatch(self, request, *args, **kwargs):
        if not groups.has_group(self.request.user, 'member'):
            return redirect("/")

        return super(EventDeleteView, self).dispatch(request, *args, **kwargs)


@login_required
def register_on_event(request, event_id):
    event_object = get_object_or_404(Event, pk=event_id)
    now = timezone.now()
    try:
        er = EventRegistration.objects.get(user=request.user, event=event_object)
        if event_object.deregistration_end > now:
            er.delete()
    except EventRegistration.DoesNotExist:
        if now > event_object.registration_start and event_object.time_end > now:
            EventRegistration.objects.create(event=event_object, user=request.user).save()

    return redirect("/events/" + event_id)

