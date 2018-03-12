from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.views.generic import TemplateView
from authentication.forms import SignUpForm
from django.contrib.auth.tokens import default_token_generator


@login_required
def logout_user(request):
    feided = request.session.get('feided', False)
    if request.user.is_authenticated:
        logout(request)
        resp = redirect(reverse('index'))
    if feided:
        print("Logging out FEIDE-user")
        resp = redirect("https://auth.dataporten.no/logout")
    return resp


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


class SignUpDoneView(TemplateView):
    template = 'redirection_page.html'

    def get_context_data(self):
        return {'title': "Registreringen var vellykket og du vil snart motta en"
                         " mail med videre instruksjoner."}
