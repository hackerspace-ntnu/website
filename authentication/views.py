from django.shortcuts import render
from authentication.forms import LoginForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse


def login_user(request):
    error_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))

    else:
        form = LoginForm()

    return render(request, 'index.html', {'form': form})


def logout_user(request):

    if request.user.is_authenticated:
        logout(request)

    return HttpResponseRedirect(reverse('index'))
