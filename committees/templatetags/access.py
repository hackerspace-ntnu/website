from django import template
from django.contrib.auth.models import Permission, AnonymousUser

register = template.Library()


@register.simple_tag
def is_committee_admin(user, committee):
    """ Test if user has admin access to the committee. """
    if user.is_superuser or user.has_perm('can_edit_committees'):
        return True
    if isinstance(user, AnonymousUser):
        return False

    # Check if user is in subcommittee with committee_admin permission. Then user is admin for parent committee.
    committee_admin = Permission.objects.get(codename="committee_admin")
    for subcommittee in committee.subcommittees.all() | committee:
        if user in subcommittee.user_set.all() and committee_admin in subcommittee.group.permissions.all():
            return True
    return False
