from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

import re

from .forms import ProfileModelFormUser, ProfileModelFormMember, ProfileModelFormAdmin
from .models import Profile, Skill, Group


def members(request):
    profiles = Profile.objects.exclude(group__isnull=True)
    if request.method == 'POST':
        text = request.POST['searchBar'].lower()
        tokens = re.split('; |, | |\n', text)

        name_results = User.objects.none()
        skill_results = Skill.objects.none()
        group_results = Group.objects.none()

        for token in tokens:
            name_results |= User.objects.filter(first_name__icontains=token) | User.objects.filter(
                last_name__icontains=token)
            skill_results |= Skill.objects.filter(title__icontains=token)
            group_results |= Group.objects.filter(title__icontains=token)

        result_profiles = [user_profile for user_profile in profiles if
                           user_profile.user in name_results or
                           any(skill in skill_results for skill in user_profile.skills.all()) or
                           any(group in group_results for group in user_profile.group.all())
                           ]

        return render(request, "userprofile/members.html", context={"profiles": result_profiles})

    return render(request, "userprofile/members.html", context={"profiles": profiles})


def skill(request, skill_title):
    skill = Skill.objects.get(title=skill_title)
    profiles = Profile.objects.filter(skills__title__icontains=skill_title, group__isnull=False).distinct()
    context = {'skill': skill, 'profiles': profiles}
    return render(request, 'userprofile/skill.html', context)


def profile(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    profile.update()
    return render(request, 'userprofile/profile.html', {'profile': profile, 'user': request.user})


def edit_profile(request):
    return edit_profile_id(request, request.user.id)


def edit_profile_id(request, profile_id):
    user = request.user
    profile = get_object_or_404(Profile, pk=profile_id)
    if user != profile.user and not user.is_superuser:
        return redirect(profile)
    if user.is_superuser:
        form = ProfileModelFormAdmin(request.POST or None, request.FILES or None, instance=profile)
    elif Profile.objects.filter(user=user, group__isnull=False):
        form = ProfileModelFormMember(request.POST or None, request.FILES or None, instance=profile)
    else:
        form = ProfileModelFormUser(request.POST or None, request.FILES or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(profile)
    return render(request, 'userprofile/edit_profile.html', {'form': form, 'profile': profile})
