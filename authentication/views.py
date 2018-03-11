from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils.http import urlsafe_base64_decode
from authentication.forms import SignUpForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect

def isFeide(request):
    return request.user.get('feided', False)


def SignUpView(request):
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
                # Send mail about activation
                form.save()
                return redirect(reverse('signup_done'))
    else:
        form = SignUpForm()

    context = {'form': form}

    return render(request, 'signup.html', context)


# Aumatically get the user model that is being used by django from its engine
UserModel = get_user_model()


def get_user(uidb64):
    try:
        # urlsafe_base64_decode() decodes to bytestring
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
        return user
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
        return user


def SignUpConfirmView(request, token, uidb64):
    # Get user based on base64 encoded ID
    user = get_user(uidb64)
    if user is not None:
        if not user.is_active:
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                message = "Din konto er aktivert!"
            else:
                message = "Linken du forsøker å bruke har utløpt."
        else:
            message = "Din konto er allerede aktivert!"
    else:
        return redirect('/')

    context = {
        'title': message
    }
    return render(request, 'redirection_page.html', context)


def SignUpDoneView(request):
    context = {
        'title': "Registreringen var vellykket og du vil snart motta\
        en mail med videre instruksjoner."
    }
    return render(request, 'redirection_page.html', context)
