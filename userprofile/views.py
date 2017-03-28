from django.shortcuts import render, redirect
import re
from .models import Profile, Group
from .forms import ProfileForm, ProfileModelForm


def members(request):
    profiles = Profile.objects.all()
    groups = Group.objects.prefetch_related('members')
    if request.method == 'POST':
        #TODO Noe her...
        text = request.POST['searchBar'].lower()
        tokens = re.split('; |, |  |\n', text)
        result_profiles = []
        for profile in profiles:
            if profile.user.first_name.lower() in tokens and profile not in result_profiles:
                result_profiles.append(profile)
            if profile.user.last_name.lower() in tokens and profile not in result_profiles:
                result_profiles.append(profile)
            for skill in profile.skills.all():
                if skill in tokens and profile not in result_profiles:
                    result_profiles.append(profile)
        return render(request, "members.html", context={"profiles": result_profiles})
    return render(request, "members.html", context={"profiles": profiles, "groups": groups})


def group(request):
    context = {'group': request.path.split("/")[-1]}
    return render(request, "group.html", context)


def profile(request):
    profile = request.user.profile
    return render(request, 'profile.html', {'profile': profile})


def edit_profile(request):
    user = request.user
    profile = user.profile
    # if this is a POST request we need to process the form data
    form = ProfileModelForm(request.POST or None, instance=profile)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        # check whether it's valid:
        if form.is_valid():
            profile.save()
            return redirect('/members/profile/')
    return render(request, 'edit_profile.html', {'form': form, 'profile': profile})
