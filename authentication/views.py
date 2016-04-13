from django.shortcuts import render
from authentication.forms import LoginForm, ChangePasswordForm, SignUpForm, ForgotPasswordForm, SetPasswordForm
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.admin import User
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from website.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from . models import UserAuthentication
from threading import Thread
from uuid import UUID
import time
from django_user_agents.utils import get_user_agent
from news.models import Article, Event
from door.models import DoorStatus


def login_user(request):
    event_list = Event.objects.order_by('-time_start')[:3]
    article_list = Article.objects.order_by('-pub_date')[:3]
    try:
        door_status = DoorStatus.objects.get(name='hackerspace').status
    except DoorStatus.DoesNotExist:
        door_status = True

    user_agent = get_user_agent(request)
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
                    error_message = 'User is not activated'
            else:
                error_message = 'Username or password is incorrect'
        else:
            error_message = 'Invalid input'
    else:
        form = LoginForm()

    context = {
        'article_list': article_list,
        'event_list': event_list,
        'form': form,
        'door_status': door_status,
        'error_message': error_message,
        'mobile': user_agent.is_mobile,
    }

    return render(request, 'index.html', context)


def login_mobile(request):
    user_agent = get_user_agent(request)
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
                error_message = 'Username or password is incorrect'
        else:
            error_message = 'Invalid input'
    else:
        form = LoginForm()

    context = {
        'form': form,
        'error_message': error_message,
        'mobile': user_agent.is_mobile,
    }

    return render(request, 'login_mobile.html', context)


def logout_user(request):

    if request.user.is_authenticated:
        logout(request)

    return HttpResponseRedirect(reverse('index'))


def change_password(request):
    user_agent = get_user_agent(request)
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

    context = {
        'form': form,
        'error_message': error_message,
        'mobile': user_agent.is_mobile,
    }
    return render(request, 'change_password.html', context)


def change_password_done(request):
    return render(request, 'change_password_done.html')


def signup(request):
    user_agent = get_user_agent(request)
    error_message = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            confirm_new_password = form.cleaned_data['confirm_new_password']

            try:
                user = User.objects.get(username=username)
                error_message = 'Username already exists'
                context = {
                    'form': form,
                    'error_message': error_message,
                    'mobile': user_agent.is_mobile,
                }
                return render(request, 'signup.html', context)
            except User.DoesNotExist:
                pass

            try:
                user = User.objects.get(email=email)
                error_message = 'Email is already registered'
                context = {
                    'form': form,
                    'error_message': error_message,
                    'mobile': user_agent.is_mobile,
                }
                return render(request, 'signup.html', context)
            except User.DoesNotExist:
                pass

            if not new_password == confirm_new_password:
                error_message = 'Passwords does not match'
                context = {
                    'form': form,
                    'error_message': error_message,
                    'mobile': user_agent.is_mobile,
                }
                return render(request, 'signup.html', context)

            if str(email).endswith('@stud.ntnu.no') or str(email).endswith('@ntnu.no') or str(email).endswith('@ntnu.edu'):

                user = User.objects.create(username=username,
                                           email=email,
                                           first_name=first_name,
                                           last_name=last_name,)
                user.set_password(new_password)
                user.is_active = False
                user.save()

                auth_object = UserAuthentication.objects.create(user=user)
                auth_object.save()
                email_subject = 'Account @ hackerspace NTNU'
                message = 'Congratulations! Your user is created. Activate your user account trough this link'
                email_message = render_to_string('signup_mail.html', {'request': request, 'message': message, 'hash_key': auth_object.key.hex})
                thread = Thread(target=send_password_email, args=(email_subject, email_message, email))
                thread.start()

                return HttpResponseRedirect(reverse('signup_done'))

            else:
                error_message = 'You need to use an NTNU email'
                context = {
                    'form': form,
                    'error_message': error_message,
                    'mobile': user_agent.is_mobile,
                }
                return render(request, 'signup.html',  context)

    else:
        form = SignUpForm()

    context = {
        'form': form,
        'error_message': error_message,
        'mobile': user_agent.is_mobile,
    }
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


def signup_done(request):
    user_agent = get_user_agent(request)
    context = {
        'mobile': user_agent.is_mobile,
    }
    return render(request, 'signup_done.html', context)


def forgot_password(request):
    user_agent = get_user_agent(request)
    error_message = None
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                error_message = 'User does not exist'
                context = {
                    'form': form,
                    'error_message': error_message,
                    'mobile': user_agent.is_mobile,
                }
                return render(request, 'forgot_password.html', context)
            else:

                auth_object = UserAuthentication.objects.create(user=user)
                auth_object.save()
                email_subject = 'New password @ hackerspace-ntnu.no'
                message = "Use this link to set a new password"
                email_message = render_to_string('signup_mail.html', {'request': request, 'message': message, 'hash_key': auth_object.key.hex},)
                thread = Thread(target=send_password_email, args=(email_subject, email_message, email))
                thread.start()

                return HttpResponseRedirect(reverse('forgot_password_done'))

        else:
            error_message = "Invalid input!"

    else:
        form = ForgotPasswordForm()

    context = {
        'form': form,
        'error_message': error_message,
        'mobile': user_agent.is_mobile,
    }
    return render(request, 'forgot_password.html', context)


def forgot_password_done(request):
    user_agent = get_user_agent(request)
    context = {
        'mobile': user_agent.is_mobile,
    }
    return render(request, 'forgot_password_done.html', context)


def activate_account(request, hash_key):
    user_agent = get_user_agent(request)
    error_message = None
    try:
        value = UUID(hash_key, version=4)
        auth_object = get_object_or_404(UserAuthentication, key=hash_key)
        if auth_object.expired():
            raise Http404
        if auth_object.user.is_active:
            if request.method == 'POST':
                form = SetPasswordForm(request.POST)
                if form.is_valid():
                    password = form.password_matches()
                    if password:
                        auth_object.set_password(password)

                        return HttpResponseRedirect(reverse('set_password_done'))
                    else:
                        error_message = 'Passwords does not match'

            else:
                form = SetPasswordForm()

            context = {
                'form': form,
                'error_message': error_message,
                'mobile': user_agent.is_mobile,
                'hash_key': hash_key,
            }
            return render(request, 'set_password.html', context)
        else:
            auth_object.activate()
            return render(request, 'activation_done.html')

    except ValueError:
        raise Http404


def set_password_done(request):
    user_agent = get_user_agent(request)
    context = {
        'mobile': user_agent.is_mobile,
    }
    return render(request, 'set_password_done.html', context)
