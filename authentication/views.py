from threading import Thread
from uuid import UUID

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.admin import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template.loader import render_to_string

from authentication.forms import LoginForm, ChangePasswordForm, SignUpForm, ForgotPasswordForm, SetPasswordForm
from website.settings import EMAIL_HOST_USER
from .models import UserAuthentication


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if form.validate():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

    else:
        form = LoginForm()

    context = {
        'form': form,
    }

    return render(request, 'login.html', context)


@login_required
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def change_password(request):
    error_message = None
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():

            # Validation of the passwords
            if form.validate(request.user):
                request.user.set_password(form.cleaned_data['new_password'])
                request.user.save()
                return HttpResponseRedirect(reverse('change_password_done'))
    else:
        form = ChangePasswordForm()

    context = {
        'form': form,
        'error_message': error_message,
    }
    return render(request, 'change_password.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            if form.validate():
                username = form.cleaned_data['username']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                new_password = form.cleaned_data['new_password']

                # Create user
                user = User.objects.create(username=username,
                                           email=email,
                                           first_name=first_name,
                                           last_name=last_name, )
                user.set_password(new_password)
                user.is_active = False
                user.save()

                # Create authentication object for activation
                auth_object = UserAuthentication.objects.create(user=user)
                auth_object.save()

                # Send mail about activation
                email_subject = 'Bruker @ hackerspace NTNU'
                message = 'Gratulerer! Du har nå laget deg en bruker hos Hackerspace NTNU.' \
                          ' Aktiver brukeren ved å trykke på følgende link: '
                email_message = render_to_string('signup_mail.html', {'request': request, 'message': message,
                                                                      'hash_key': auth_object.key.hex})
                thread = Thread(target=send_password_email, args=(email_subject, email_message, email))
                thread.start()

                return HttpResponseRedirect(reverse('signup_done'))

    else:
        form = SignUpForm()

    context = {'form': form}

    return render(request, 'signup.html', context)


def send_password_email(subject, message, email):
    print("SENDING MAIL")
    send_mail(subject,
              message,
              '%s'.format(EMAIL_HOST_USER),
              [email],
              fail_silently=False,
              html_message=message)

    print("MAIL SENT")


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            print("FORM IS VALID")
            if form.validate():
                print("VALIDATED")
                email = form.cleaned_data['email']

                # Create authentication object for verification of new password
                user = User.objects.get(email=email)
                auth_object = UserAuthentication.objects.create(user=user)
                auth_object.save()

                # Send forgot password link
                email_subject = 'Nytt passord @ hackerspace-ntnu.no'
                message = "Trykk på følgende link for å sette deg et nytt passord: "
                email_message = render_to_string('signup_mail.html', {'request': request, 'message': message,
                                                                      'hash_key': auth_object.key.hex}, )
                thread = Thread(target=send_password_email, args=(email_subject, email_message, email))
                thread.start()

                return HttpResponseRedirect(reverse('forgot_password_done'))

    else:
        form = ForgotPasswordForm()

    context = {
        'form': form,
    }

    return render(request, 'forgot_password.html', context)


def activate_account(request, hash_key):
    # Check if the hash_key is in the database
    try:
        UUID(hash_key, version=4)
        auth_object = get_object_or_404(UserAuthentication, key=hash_key)
        if auth_object.expired():
            raise Http404

        # Checks if the authentication object is valid and validates the userinput
        if auth_object.user.is_active:
            if request.method == 'POST':
                form = SetPasswordForm(request.POST)
                if form.is_valid():
                    if form.validate():
                        auth_object.set_password(form.cleaned_data["password"])
                        return HttpResponseRedirect(reverse('set_password_done'))

            else:
                form = SetPasswordForm()

            context = {
                'form': form,
                'hash_key': hash_key,
            }
            return render(request, 'set_password.html', context)
        else:
            auth_object.activate()
            context = {
                'message': "Brukeren er nå aktiv, du vil snart bli videresendt."
            }
            return render(request, 'redirection_page.html', context)

    except ValueError:
        raise Http404


def set_password_done(request):
    context = {
        'message': "Ditt passord er nå endret, du vil snart bli videresendt."
    }
    return render(request, 'redirection_page.html', context)


def change_password_done(request):
    context = {
        'message': "Ditt passord er nå endret, du vil snart bli videresendt."
    }
    return render(request, 'redirection_page.html', context)


def forgot_password_done(request):
    context = {
        'message': "Du vil snart motta en mail med videre instruksjoner."
    }
    return render(request, 'redirection_page.html', context)


def signup_done(request):
    context = {
        'message': "Registreringen var vellykket og du vil snart motta en mail med videre instruksjoner."
    }
    return render(request, 'redirection_page.html', context)
