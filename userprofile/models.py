from typing import Iterable, List

from bleach import clean
from bleach_whitelist import markdown_attrs, markdown_tags
from django.contrib.auth.admin import User
from django.core.files.base import ContentFile
from django.db import models
from django.db.models import Q
from django.shortcuts import reverse
from django.utils import timezone
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from sorl.thumbnail import get_thumbnail

from applications.validators import validate_phone_number
from committees.models import Committee


class TermsOfService(models.Model):

    text = MarkdownxField()
    pub_date = models.DateField(default=timezone.now, verbose_name="Publiseringsdato")

    def __str__(self):
        return self.pub_date.strftime("%d. %B %Y")

    def body_formatted_markdown(self):
        return clean(markdownify(self.text), markdown_tags, markdown_attrs)


class Skill(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField()
    thumb = models.ForeignKey(
        "files.Image", blank=True, null=True, on_delete=models.SET_NULL
    )

    categories = models.ManyToManyField(blank=False, to="userprofile.Category")

    prerequisites = models.ManyToManyField(blank=True, to="userprofile.Skill")

    def __str__(self):
        return (
            self.name
            + " ("
            + ", ".join(category.name for category in self.categories.all())
            + ")"
        )


class Category(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField()
    thumb = models.ForeignKey(
        "files.Image", blank=True, null=True, on_delete=models.SET_NULL
    )

    color = models.CharField(max_length=20, default="", blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class ProfileManager(models.Manager):
    def search(self, query: str = None):
        qs = self.get_queryset().filter(
            user__groups__name__in=Committee.objects.values_list("name", flat=True)
        )
        if query is not None:
            or_lookup = (
                Q(user__username__icontains=query)
                | Q(user__first_name__icontains=query)
                | Q(user__last_name__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="profilepictures",
        verbose_name="Profilbilde",
        default=None,
        blank=True,
    )

    skills = models.ManyToManyField(
        blank=True, verbose_name="Ferdigheter", to="userprofile.Skill"
    )

    # Felter for sosiale konti
    social_discord = models.CharField(
        max_length=30, null=True, blank=True, verbose_name="Discord-tag"
    )
    social_steam = models.CharField(
        max_length=30, null=True, blank=True, verbose_name="Steam navn"
    )
    social_battlenet = models.CharField(
        max_length=30, null=True, blank=True, verbose_name="Battle.net-tag"
    )
    social_git = models.CharField(
        max_length=30, null=True, blank=True, verbose_name="Github brukernavn"
    )

    limit_social = models.BooleanField(
        default=False,
        verbose_name="Vis sosiale profiler kun for andre Hackerspace-medlemmer",
    )

    study = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Studieretning"
    )

    accepted_tos = models.ForeignKey(
        TermsOfService,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Seneste aksepterte TOS",
    )

    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        validators=[validate_phone_number],
        verbose_name="Telefonnummer",
        help_text="Brukes til reservasjonssystem i tilfelle du må kontaktes.",
    )

    show_email = models.BooleanField(
        default=False, verbose_name="Vis e-postadresse i din profil"
    )

    allergi_gluten = models.BooleanField(
        default=False, verbose_name="Ønsker glutenfritt alternativ"
    )
    allergi_vegetar = models.BooleanField(
        default=False, verbose_name="Ønsker vegetar alternativ"
    )
    allergi_vegan = models.BooleanField(
        default=False, verbose_name="Ønsker vegansk alternativ"
    )
    allergi_annet = models.CharField(
        max_length=140,
        null=True,
        blank=True,
        verbose_name="Evt. andre ønsker for matservering.",
    )

    objects = ProfileManager()

    class Meta:
        permissions = (
            ("is_active_member", "Is an active member. Catchall permission"),
            ("can_view_social", "Can see social fields on UserProfile"),
            ("can_view_admin", "Can see information for admin panel"),
        )

    def save(self, *args, **kwargs):
        if self.image:
            # Make sure image is saved before tumbnailing
            super(Profile, self).save(*args, **kwargs)
            thumb = get_thumbnail(self.image, "300x300", crop="center", quality=99)
            self.image.save(thumb.name, ContentFile(thumb.read()), False)
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def get_main_group(self):
        # Assumes first committee (usually just one) is the main group, with fallback to first group if no committees
        return (
            Committee.objects.filter(group_ptr__in=self.user.groups.all()).first()
            or self.user.groups.first()
        )

    def get_absolute_url(self):
        return reverse("userprofile:profile", args=(self.pk,))

    def get_food_preferences(self):

        preferences_of_predefined = []

        if self.allergi_gluten:
            preferences_of_predefined.append("glutenfritt")
        if self.allergi_vegetar:
            preferences_of_predefined.append("vegetar")
        if self.allergi_vegan:
            preferences_of_predefined.append("vegan")

        return {"predefined": preferences_of_predefined, "other": self.allergi_annet}

    def has_food_preferences(self):
        return (
            self.allergi_gluten
            or self.allergi_vegetar
            or self.allergi_vegan
            or self.allergi_annet
        )

    def has_accepted_most_recent_tos(self):
        return self.accepted_tos == TermsOfService.objects.order_by("-pub_date").first()

    def has_skills(self, skills: Iterable[Skill]) -> bool:
        for skill in skills:
            if skill not in self.skills.all():
                return False
        return True

    def is_unreachable_skill(self, skill):
        return skill.prerequisites.exclude(id__in=self.skills.all()).exists()

    # Retrieves skills that can be acquired without intermediate skills
    def get_reachable_skills(self):
        return self.filter_skills_reachability(
            Skill.objects.exclude(id__in=self.skills.all()), reachable=True
        )

    # Filters skills based on whether they can be acquired without intermediate skills
    def filter_skills_reachability(
        self, skills: Iterable[Skill], reachable: bool
    ) -> List[Skill]:
        filtered_skills = []

        for skill in skills:
            if reachable ^ self.is_unreachable_skill(skill):
                filtered_skills.append(skill)

        return filtered_skills
