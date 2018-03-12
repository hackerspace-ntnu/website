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
    is_feide_login = request.session.get('feided', False)
    logout(request)
    if is_feide_login:
        return redirect("https://auth.dataporten.no/logout")
    return redirect(reverse('index'))


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


# Automatically get the user model that is being used by django from its engine
UserModel = get_user_model()


def get_user(uidb64):
    try:
        # urlsafe_base64_decode() decodes to bytestring
        uid = urlsafe_base64_decode(uidb64).decode()
        return UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        return None


class SignUpConfirmView(TemplateView):
    template = 'redirection_page.html'

    def dispatch(self, *args, **kwargs):
        # If the user id is does not exist redirect to the main page
        if get_user(kwargs['uidb64']) is None:
            return redirect('/')
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        user = get_user(kwargs['uidb64'])
        if user.is_active:
            return {'title': 'Din konto er allerede aktivert!'}
        if default_token_generator.check_token(user, kwargs["token"]):
            user.is_active = True
            user.save()
            return {'title': 'Din kont er aktivert!'}
        return {'title': "Linken du forsøker å bruker har utløpt"}


class SignUpDoneView(TemplateView):
    template = 'redirection_page.html'

    def get_context_data(self):
        return {'title': "Registreringen var vellykket og du vil snart motta en"
                         " mail med videre instruksjoner."}
