from django.shortcuts import render
from authentication.forms import LoginForm, ChangePasswordForm
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

    return HttpResponseRedirect(reverse('index'))


def logout_user(request):

    if request.user.is_authenticated:
        logout(request)

    return HttpResponseRedirect(reverse('index'))


def change_password(request):
    error_message = None
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            confirm_new_password = form.cleaned_data['confirm_new_password']
            if request.user.check_password(current_password) and new_password == confirm_new_password:
                request.user.set_password(new_password)
                request.user.save()
                return HttpResponseRedirect(reverse('change_password_done'))
            else:
                error_message = "Password does not match!"
        else:
            error_message = "Invalid input!"

    else:
        form = ChangePasswordForm()

    return render(request, 'change_password.html', {'form': form,
                                                    'error_message': error_message})


def change_password_done(request):
    return render(request, 'change_password_done.html')
