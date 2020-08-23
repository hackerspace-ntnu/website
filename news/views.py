from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from datetime import datetime
from .forms import EventForm, eventformset, uploadformset
from .models import Event, Article, EventRegistration
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class EventView(DetailView):
    model = Event
    template_name = "news/event.html"

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().internal and not request.user.has_perm('news.can_view_internal_event'):

            # Stores log-in prompt message to be displayed with redirect request
            messages.add_message(request, messages.WARNING, 'Logg inn for å se internt arrangement')

            return redirect("/")

        return super(EventView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['userstatus'] = "ikke pålogget"
        context_data['expired_event'] = datetime.now() > self.object.time_end

        if self.request.user.is_authenticated:
            context_data['userstatus'] = self.object.userstatus(self.request.user)
            if(self.object.is_waiting(self.request.user)):
                context_data['get_position'] = "Du er nummer " + str(self.object.get_position(user=self.request.user)) + " på ventelisten"
            else:
                context_data['get_position'] = "Du er ikke på ventelisten."

        return context_data


class EventListView(ListView):
    template_name = "news/events.html"
    paginate_by = 10

    def get_internal_events_indicator(self):

        current_date = datetime.now()

        # Determine number of hidden internal events
        if not self.request.user.has_perm('news.can_view_internal_event'):
            upcoming_internal_events_count = len(Event.objects.filter(internal=True).filter(time_start__gte=current_date))
            return "Du har ikke rettigheter til å se interne arrangementer."

        return None

    def get_queryset(self):
        if self.request.user.has_perm('news.can_view_internal_event'):
            return Event.objects.order_by('-time_end')
        else:
            return Event.objects.filter(internal=False).order_by('-time_end')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['indicator_text'] = self.get_internal_events_indicator()

        return context


class EventAttendeeEditView(PermissionRequiredMixin, UpdateView):
    '''
        Denne klassen lar deg liste opp alle deltakere i en event og deretter huke av om
        de har møtt opp eller ikke.
    '''
    template_name = "news/attendee_form.html"
    model = Event
    fields = ['title']
    permission_required = "news.can_see_attendees"

    def get_context_data(self, **kwargs):
        context = super(EventAttendeeEditView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['registrations'] = eventformset(self.request.POST, instance=self.object)
        else:
            context['registrations'] = eventformset(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['registrations']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse('events:details', kwargs={'pk': self.object.id})


class ArticleListView(ListView):
    template_name = "news/news.html"
    paginate_by = 10

    def get_internal_articles_indicator(self):

        # Determine number of hidden internal articles
        if not self.request.user.has_perm('news.can_view_internal_article'):
            internal_articles_count = len(Article.objects.filter(internal=True))
            return "Du har ikke rettigheter til å se interne artikler."

        return None


    def get_queryset(self):
        if self.request.user.has_perm("news.can_view_internal_article"):
            return Article.objects.order_by('-pub_date')
        else:
            return Article.objects.filter(internal=False).order_by('-pub_date')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['indicator_text'] = self.get_internal_articles_indicator()

        return context



class ArticleView(DetailView):
    model = Article
    template_name = "news/article.html"

    def dispatch(self, request, *args, **kwargs):

        # If the article is internal, check if user has the permission to view.
        if self.get_object().internal and not request.user.has_perm("news.can_view_internal_article"):

            # Stores log-in prompt message to be displayed with redirect request
            messages.add_message(request, messages.WARNING, 'Logg inn for å se intern artikkel')

            return redirect("/")

        return super(ArticleView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # Check user internal article view permission
        can_access_internal_article = self.request.user.has_perm('news.can_view_internal_article')

        # Get permitted articles
        article_list = Article.objects.filter(internal__lte=can_access_internal_article)

        # Get oldest article that is newer than current (None if current is latest)
        next_article = article_list.filter(pub_date__gt=self.get_object().pub_date).order_by('pub_date').first()

        # Get latest article that is older than current (None if current is oldest)
        previous_article = article_list.filter(pub_date__lt=self.get_object().pub_date).order_by('-pub_date').first()

        context['next_article'] = next_article
        context['previous_article'] = previous_article

        return context



class EventUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Event
    template_name = "news/edit_event.html"
    form_class = EventForm
    permission_required = 'news.change_event'
    success_message = "Arrangementet er oppdatert."

    def get_context_data(self, **kwargs):
        context = super(EventUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['uploads_form'] = uploadformset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['uploads_form'] = uploadformset(instance=self.object)

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        context = self.get_context_data()

        upload_form = context['uploads_form']

        if upload_form.is_valid():
            self.object = form.save()
            upload_form.instance = self.object
            upload_form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            errors = upload_form.errors
            raise
            return self.render_to_response(self.get_context_data(form=form))


    def get_initial(self):
        initial = super(EventUpdateView, self).get_initial()
        initial['time_start'] = self.object.time_start
        initial['time_end'] = self.object.time_end
        initial['registration_start'] = self.object.registration_start
        initial['registration_end'] = self.object.registration_end
        initial['deregistration_end'] = self.object.deregistration_end
        return initial

    def get_success_url(self):
        return reverse('events:details', kwargs={'pk': self.object.id})


class EventCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Event
    template_name = "news/edit_event.html"
    form_class = EventForm
    success_url = "/events/"
    permission_required = 'news.add_event'
    success_message = "Arrangementet er opprettet og publisert."

    def get_success_url(self):
        return reverse('events:details', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(EventCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['uploads_form'] = uploadformset(self.request.POST, self.request.FILES)
        else:
            context['uploads_form'] = uploadformset(instance=self.object)
        return context

    def get_initial(self):
        initial = super(EventCreateView, self).get_initial()
        initial['time_start'] = timezone.now()
        initial['time_end'] = timezone.now()

        initial['registration_start'] = timezone.now()
        initial['registration_end'] = timezone.now()
        initial['deregistration_end'] = timezone.now()
        return initial

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save(commit=False)
        context = self.get_context_data()

        upload_form = context['uploads_form']

        if upload_form.is_valid():
            self.object = form.save()
            upload_form.instance = self.object
            upload_form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))



class ArticleCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Article
    fields = ['title', 'ingress_content', 'main_content', 'thumbnail', 'internal']
    template_name = "news/edit_article.html"
    permission_required = "news.add_article"
    success_message = "Artikkelen er opprettet og publisert."

    def get_success_url(self):
        return reverse('news:details', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ArticleUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Article
    template_name = "news/edit_article.html"
    fields = ['title', 'ingress_content', 'main_content', 'thumbnail', 'internal']
    permission_required = "news.change_article"
    success_message = "Artikkelen er oppdatert."

    def get_success_url(self):
        return reverse('news:details', kwargs={'pk': self.object.id})


class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    model = Article
    success_url = "/news/"
    permission_required = "news.delete_article"


class EventDeleteView(PermissionRequiredMixin, DeleteView):
    model = Event
    success_url = "/events/"
    permission_required = "news.delete_event"


@login_required
def register_on_event(request, event_id):
    event_object = get_object_or_404(Event, pk=event_id)
    now = timezone.now()
    try:
        er = EventRegistration.objects.get(user=request.user, event=event_object)
        if event_object.deregistration_end > now:
            er.delete()
            messages.add_message(request, messages.SUCCESS, 'Du er nå avmeldt')
    except EventRegistration.DoesNotExist:
        if now > event_object.registration_start and event_object.time_end > now:
            EventRegistration.objects.create(event=event_object, user=request.user).save()
            messages.add_message(request, messages.SUCCESS, 'Du er nå påmeldt')

    return redirect("/events/" + str(event_id))
