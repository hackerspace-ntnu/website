from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from social_core.exceptions import AuthException

from userprofile.models import Profile


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse("index"))


def save_profile(backend, user, response, is_new=False, *args, **kwargs):
    if backend.name == "dataporten_feide":
        if is_new:
            first, last = response.get("fullname").split(" ", 1)

            user.first_name = first
            user.last_name = last
            user.email = response.get("username")

            try:
                user.profile
            except Profile.DoesNotExist:
                Profile.objects.create(user=user)

            user.save()
        else:
            try:
                user.profile
            except Profile.DoesNotExist:
                Profile.objects.create(user=user)


def associate_by_email(backend, details, user=None, *args, **kwargs):
    """
    Associate current auth with a user with the same email address in the DB.
    This pipeline entry is not 100% secure unless you know that the providers
    enabled enforce email verification on their side, otherwise a user can
    attempt to take over another user account by using the same (not validated)
    email address on some provider.  This pipeline entry is disabled by
    default.
    """
    if user:
        return None

    email = details.get("username")

    # In case its an older account with stud.ntnu.no
    alt_email = email.split("@")[0] + "@stud.ntnu.no"

    if email:
        # Try to associate accounts registered with the same email address,
        # only if it's a single object. AuthException is raised if multiple
        # objects are returned.
        users = list(backend.strategy.storage.user.get_users_by_email(email))
        alt_users = list(backend.strategy.storage.user.get_users_by_email(alt_email))

        if len(users) == 0 and len(alt_users) == 0:
            return None
        elif len(users) > 1 or len(alt_users) > 1:
            raise AuthException(
                backend, "The given email address is associated with another account"
            )
        else:
            if len(users) == 1:
                return {"user": users[0], "is_new": False}
            if len(alt_users) == 1:
                # Convert old user to new feide email syntax
                prison_user = alt_users[0]
                prison_user.email = email
                prison_user.save()

                return {"user": alt_users[0], "is_new": False}
