from django.shortcuts import render
from .models import Profile, Group


def profile(request):
    profiles = Profile.objects.all()
    groups = Group.objects.prefetch_related('members')
    return render(request, "userprofile.html", context={"profiles": profiles, "groups": groups})
