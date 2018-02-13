from ckeditor.fields import RichTextField
from django.contrib.auth.models import Group, User
from django.core.urlresolvers import reverse
from django.db import models
from files.models import Image


class Committee(Group):
    # Har name fra superklassen
    email = models.EmailField(null=True, blank=True)
    thumbnail = models.ForeignKey(Image, on_delete=models.SET_NULL, blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    visible = models.BooleanField(default=True)

    one_liner = models.CharField(max_length=30, verbose_name="Lynbeskrivelse")
    header = models.CharField(max_length=150, verbose_name="Overskrift", blank=True, null=True)
    description = RichTextField(verbose_name='Beskrivelse', config_name='committees')

    parent = models.ForeignKey('Committee', null=True, blank=True, related_name="subcommittees")
    # Har Many2ManyField til Permission i superklasse

    class Meta:
        permissions = (
            ("can_edit_committees", "Can edit all committees"),
            ("committee_admin", "Can edit this committee and parent committee."),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('verv:view', kwargs={'slug':self.slug})

    def add_user(self, user):
        if user not in self.user_set.all():
            self.user_set.add(user)
            self.save()
            if self.parent is not None:
                self.parent.add_user(user)

    def remove_user(self, user):
        if user in self.user_set.all():
            self.user_set.remove(user)
            self.save()
            for subcommittee in self.subcommittees.all():
                subcommittee.remove_user(user)
