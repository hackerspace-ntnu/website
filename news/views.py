from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from datetime import datetime, timedelta
from .forms import EventForm, eventformset, uploadformset, ArticleForm
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

        event = self.get_object()

        if event.internal and not request.user.has_perm('news.can_view_internal_event'):

            # Stores log-in prompt message to be displayed with redirect request
            messages.add_message(request, messages.WARNING, 'Logg inn for å se internt arrangement')

            return redirect("/")

        # If the event is a draft, check if user is the author
        if event.draft and not request.user == event.author:

            # Stores log-in prompt message to be displayed with redirect request
            messages.add_message(request, messages.WARNING, 'Du har ikke tilgang til arrangementet')

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

        if not self.request.user.has_perm('news.can_view_internal_event'):
            return "Du har ikke rettigheter til å se interne arrangementer."

        return None

    def get_queryset(self):

        # Retrieve published events (so no drafts)
        events = Event.objects.order_by('-time_end').filter(draft=False)

        # Decide if visitor should see internal events
        if self.request.user.has_perm('news.can_view_internal_event'):
            return events
        else:
            return events.filter(internal=False)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['indicator_text'] = self.get_internal_events_indicator()

        # Retrieve any user drafts if logged in
        if self.request.user.has_perm("news.add_event"):
            context['drafts'] = Event.objects.order_by('-time_end').filter(author=self.request.user, draft=True)

        return context


class EventAttendeeEditView(PermissionRequiredMixin, UpdateView):
    """
        Denne klassen lar deg liste opp alle deltakere i en event og deretter huke av om
        de har møtt opp eller ikke.
    """
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

        if not self.request.user.has_perm('news.can_view_internal_article'):
            return "Du har ikke rettigheter til å se interne artikler."

        return None


    def get_queryset(self):
        # Retrieve published articles (so no drafts)
        articles = Article.objects.order_by('-pub_date').filter(draft=False)

        # Decide if visitor should see internal articles
        if self.request.user.has_perm("news.can_view_internal_article"):
            return articles
        else:
            return articles.filter(internal=False)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['indicator_text'] = self.get_internal_articles_indicator()

        # Retrieve any user drafts if logged in
        if self.request.user.has_perm("news.add_article"):
            context['drafts'] = Article.objects.order_by('-pub_date').filter(author=self.request.user,draft=True)

        return context



class ArticleView(DetailView):
    model = Article
    template_name = "news/article.html"

    def dispatch(self, request, *args, **kwargs):

        article = self.get_object()

        # If the article is internal, check if user has the permission to view.
        if self.get_object().internal and not request.user.has_perm("news.can_view_internal_article"):

            # Stores log-in prompt message to be displayed with redirect request
            messages.add_message(request, messages.WARNING, 'Logg inn for å se intern artikkel')

            return redirect("/")

        # If the article is a draft, check if user is the author
        if article.draft and not request.user == article.author:

            # Stores log-in prompt message to be displayed with redirect request
            messages.add_message(request, messages.WARNING, 'Du har ikke tilgang til artikkelen')

            return redirect("/")

        return super(ArticleView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # Check user internal article view permission
        can_access_internal_article = self.request.user.has_perm('news.can_view_internal_article')

        # Get permitted articles
        article_list = Article.objects.filter(internal__lte=can_access_internal_article,draft=False)

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

    def get_success_message(self, cleaned_data):
        if self.object.draft:
            return "Arrangementet er opprettet som utkast"
        return "Arrangementet er opprettet og publisert"

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
        initial['registration_end'] = timezone.now() + timedelta(days=7)
        initial['deregistration_end'] = timezone.now() + timedelta(days=7)
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
    form_class = ArticleForm
    template_name = "news/edit_article.html"
    permission_required = "news.add_article"

    def get_success_message(self, cleaned_data):
        if self.object.draft:
            return "Artikkelen er opprettet som utkast"
        return "Artikkelen er opprettet og publisert"

    def get_success_url(self):
        return reverse('news:details', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "news/edit_article.html"
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
