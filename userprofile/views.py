from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import re

from .models import Profile, Skill, Group
from .forms import ProfileForm, ProfileModelForm


def members(request):
    profiles = Profile.objects.all()
    #groups = Group.objects.prefetch_related('members')
    if request.method == 'POST':
        text = request.POST['searchBar'].lower()
        tokens = re.split('; |, |  |\n', text)
        result_profiles = []

        # User.objects.filter(first_name__lower__contains=token)


        for token in tokens:
            first_name_results = User.objects.filter(first_name__icontains=token)
            last_name_results = User.objects.filter(last_name__icontains=token)
            skill_results = Skill.objects.filter(title__icontains=token)
            group_results = Group.objects.filter(title__icontains=token)

        for profile in profiles:
            if profile.user in first_name_results or profile.user in last_name_results:
                result_profiles.append(profile)
            for skill in profile.skills.all():
                if skill in skill_results and profile not in result_profiles:
                    result_profiles.append(profile)
            for group in profile.group.all():
                if group in group_results and profile not in result_profiles:
                    result_profiles.append(profile)
        return render(request, "members.html", context={"profiles": result_profiles})

    return render(request, "members.html", context={"profiles": profiles})#, "groups": groups})


"""
def skill(request):
    skill = request.path.split('/')[-1]
    profiles = []
    for profile in Profile.objects.all():
        for s in profile.skills.all():
            if str(s).lower() == str(skill).lower():
                profiles.append(profile)
    context = {'skill': skill, 'profiles': profiles}
    return render(request, 'skill.html', context)


def group(request):
    context = {'group': request.path.split("/")[-1]}
    return render(request, "group.html", context)

"""
def profile(request, profileID):
    profile = Profile.objects.get(user_id=profileID)
    profile.update()
    return render(request, 'profile.html', {'profile': profile, 'user': request.user })

def edit_profile(request):
    user = request.user
    profile = user.profile
    form = ProfileModelForm(request.POST or None, instance=profile)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/members/profile/'+str(profile.user_id))
    return render(request, 'edit_profile.html', {'form': form, 'profile': profile})

def edit_profile_id(request,profileID):
    user = request.user
    profile = Profile.objects.get(user_id=profileID)
    if user!=profile.user and not user.is_superuser:
        return redirect('/members/profile/'+str(profileID))
    form = ProfileModelForm(request.POST or None, instance=profile)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/members/profile/'+str(profileID))
    return render(request, 'edit_profile.html', {'form': form, 'profile': profile})
