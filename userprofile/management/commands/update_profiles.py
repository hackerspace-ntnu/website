from django.core.management.base import BaseCommand, CommandError
from userprofile.models import Profile
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Updatje profiles for all users"

    def add_arguments(self, parser):
        parser.add_argument('users', nargs="*", type=str)

    def handle(self, *args, **options):
        if not options['users']:
            profiles = Profile.objects.all()
            for profile in profiles:
                try:
                    profile.update()
                    print("Updated profile for {}".format(profile.user.username))
                except :
                    print("Cannot update profile for {}".format(user.username))
                    
        else:
            for username in options['users']:
                try:
                    profile = Profiles.objects.get(user__username=username)
                    profile.update()
                    print("Updated profile for {}".format(profile.user.username))
                except Profile.DoesNotExist:
                    print("Cannot update profile for {}".format(user.username))
