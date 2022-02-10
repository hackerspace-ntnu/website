from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin

# For merging user and profile forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse

# For approving skills
from django.views.generic import CreateView, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

# Member list search
from rapidfuzz import fuzz
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from committees.models import Committee

from .forms import ProfileForm, ProfileSearchForm
from .models import Category, Profile, Skill, TermsOfService


def _get_user_profiles_from_search(users: [User], search: str):
    """
    Determine full name similarity for each user, and return a list of corresponding profiles, ordered by best match
    """

    search_matches = []
    for user in users:
        match_score = fuzz.token_set_ratio(user.get_full_name(), search)
        if match_score > 10:
            search_matches.append((match_score, user))
    # Order by best match, descending
    search_matches.sort(key=lambda t: t[0], reverse=True)
    # Ordered profiles
    return [s[1].profile for s in search_matches]


class MembersAPIView(APIView):
    """
    API view returning an HTML response containing paginated profiles
    based on member name search
    """

    renderer_classes = [TemplateHTMLRenderer]
    template_name = "userprofile/members_list.html"
    paginate_by = 9

    def get(self, request):
        # Start with all member users, sorted by full name
        committee_array = Committee.objects.values_list("name", flat=True)
        users = sorted(
            User.objects.filter(groups__name__in=list(committee_array)),
            key=lambda a: a.get_full_name(),
        )
        search = self.request.GET.get("s", "")
        if search == "":
            profiles = [user.profile for user in users]
        else:
            profiles = _get_user_profiles_from_search(users, search)
        # Paginate profiles
        paginator = Paginator(profiles, self.paginate_by)
        page_number = self.request.GET.get("p", 1)
        page_obj = paginator.page(page_number)
        return Response({"members": page_obj.object_list, "page_obj": page_obj})


class MembersView(ListView):
    # Lister opp alle brukerprofiler med pagination
    model = Profile
    form_class = ProfileSearchForm
    paginate_by = 9
    template_name = "userprofile/members.html"

    def get_context_data(self, **kwargs):
        context = super(MembersView, self).get_context_data(**kwargs)
        context["search"] = self.request.GET.get("s", "")
        context["page"] = self.request.GET.get("p", 1)
        return context


# Class providing a method for retrieving skill category levels
class CategoryLevelsMixin:
    def get_category_levels(self):
        # Tuple list (category, level)
        levels = []

        for category in Category.objects.all():
            # Total acquired skills in category
            level = Skill.objects.filter(
                categories__pk=category.pk, pk__in=self.object.skills.all()
            ).count()

            levels.append((category, level))

        # Sort tuple list by category level (descending)
        levels.sort(key=lambda tup: tup[1], reverse=True)

        return levels


class ProfileDetailView(DetailView, CategoryLevelsMixin):
    # Vis en spesifikk profil.
    # Endpointet her er /profile/<id>
    template_name = "userprofile/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["all_categories"] = Category.objects.all()

        context["category_levels"] = self.get_category_levels()

        return context

    def get_object(self, **kwargs):
        # Get the user for the pk, then return the user profile
        pk = self.kwargs["pk"]
        user = get_object_or_404(User, pk=pk)
        return get_object_or_404(Profile, pk=user.profile.pk)


class SelfProfileDetailView(ProfileDetailView):
    # Vis egen profil.
    # Endpointet her er /profile/
    model = Profile

    def get_object(self):
        try:
            userprofile = self.request.user.profile
            return userprofile
        except AttributeError:
            raise Http404("Profile not found")


class ProfileUpdateView(SuccessMessageMixin, UpdateView):
    # Klasse for å oppdatere brukerprofilen sin
    model = Profile
    form_class = ProfileForm
    template_name = "userprofile/edit_profile.html"
    success_url = "/profile"
    success_message = "Profilen er oppdatert."

    def get_object(self, **kwargs):
        try:
            userprofile = self.request.user.profile
            return userprofile
        except AttributeError:
            raise Http404("Profile not found")


class SkillsView(DetailView, CategoryLevelsMixin):
    template_name = "userprofile/skills.html"

    # Retrieves skills that can be acquired without intermediate skills
    def get_reachable_skills(self):

        reachable_skills = []

        # Check all unacquired skills
        for skill in Skill.objects.exclude(id__in=self.object.skills.all()):

            # Make sure all prerequisite skills are acquired
            # (checks if prerequisites set is empty after excluding acquired skills)
            if not skill.prerequisites.exclude(
                id__in=self.object.skills.all()
            ).exists():
                reachable_skills.append(skill)

        return reachable_skills

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_skills"] = Skill.objects.all()
        context["reachable_skills"] = self.get_reachable_skills()
        context["category_levels"] = self.get_category_levels()

        # Sjekker hvilke skills brukeren som er logget inn kan godkjenne
        if self.request.user.is_authenticated:
            reachable_skill_ids = [skill.pk for skill in context["reachable_skills"]]
            approvable_skills = self.request.user.profile.skills.filter(
                pk__in=reachable_skill_ids
            )
            context["approvable_skills"] = approvable_skills

        # Check if request includes specific skill id
        if "skill_pk" in self.kwargs:
            context["redirect_skill"] = Skill.objects.get(id=self.kwargs["skill_pk"])

        return context

    def get_object(self, **kwargs):
        # Get the user for the pk, then return the user profile
        pk = self.kwargs["pk"]
        user = get_object_or_404(User, pk=pk)
        return get_object_or_404(Profile, pk=user.profile.pk)


class SelfSkillsView(SkillsView):
    def get_object(self):
        try:
            userprofile = self.request.user.profile
            return userprofile
        except AttributeError:
            raise Http404("Profile not found")


class ApproveSkillAPIView(APIView):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return Response(
                {"Status": "User not logged in"}, status=status.HTTP_401_UNAUTHORIZED
            )
        approver = request.user
        try:
            user = User.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(
                {"Status": f"No user with id {pk} found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            skill_id = request.data["skill_id"]
        except KeyError:
            return Response(
                {"Status": "Request missing field skill_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            skill = Skill.objects.get(pk=skill_id)
        except ObjectDoesNotExist:
            return Response(
                {"Status": f"No skill with id {skill_id} found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if skill not in approver.profile.skills.all():
            return Response(
                {"Status": "Logged in user cannot approve that skill"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        user.profile.skills.add(skill)
        return Response({"Status": f"Skill {skill} approved for user {user}"})


class SkillsCategoryView(DetailView):
    model = Category
    template_name = "userprofile/skills_category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_skills"] = Skill.objects.filter(categories__pk=self.object.pk)
        return context


class TermsOfServiceView(DetailView):
    model = TermsOfService
    template_name = "userprofile/tos_detail.html"


class MostRecentTermsOfServiceView(RedirectView):

    # Redirect url without primary key to detail view of the latest TOS
    def get_redirect_url(self, *args, **kwargs):
        termsofservice = TermsOfService.objects.order_by("-pub_date").first()
        return reverse("tos-details", kwargs={"pk": termsofservice.id})


class TermsOfServiceCreateView(
    PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    model = TermsOfService
    fields = ["text", "pub_date"]
    template_name = "userprofile/create_tos.html"
    permission_required = "userprofile.add_termsofservice"
    success_message = "TOS er opprettet"

    def get_success_url(self):
        # Redirect to detail view of newly created TOS
        return reverse("tos-details", kwargs={"pk": self.object.id})

    def get_initial(self):
        initial = super().get_initial()

        # Check if new TOS should be based on an old TOS
        if "pk" in self.kwargs:
            # Prepopulate new TOS with text from old TOS given in URL
            initial["text"] = TermsOfService.objects.get(id=self.kwargs["pk"]).text

        return initial
