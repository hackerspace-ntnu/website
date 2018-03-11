from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils.http import urlsafe_base64_decode
from authentication.forms import SignUpForm



def SignUpView(request):
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
                # Send mail about activation
                form.save()
                return HttpResponseRedirect(reverse('signup_done'))
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
    account = get_user(uidb64)
    account.is_active = True
    account.save()

    context = {
        'title': "Du har fått aktivert din konto"
    }
    return render(request, 'redirection_page.html', context)

def SignUpDoneView(request):
    context = {
        'title': "Registreringen var vellykket og du vil snart motta en mail med videre instruksjoner."
    }
    return render(request, 'redirection_page.html', context)
