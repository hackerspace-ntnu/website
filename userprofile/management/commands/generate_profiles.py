from django.core.management.base import BaseCommand
from userprofile.models import Profile
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Generate missing profiles"

    def add_arguments(self, parser):
        parser.add_argument('users', nargs="*", type=str)

    def handle(self, *args, **options):
        if not options['users']:
            users = User.objects.all()
            for user in users:
                try:
                    profile = Profile.objects.get(user_id=user.id)
                except Profile.DoesNotExist:
                    try:
                        name = user.first_name + " " + user.last_name
                        profile = Profile.objects.create(user=user, name=name, auto_duty=True, auto_name=True)
                        profile.update()
                        print("Created profile for {}".format(user.username))
                    except:
                        print("Cannot create profile for {}".format(user.username))

        else:
            for username in options['users']:
                try:
                    profile = Profile.objects.get(user__username=username)
                except Profile.DoesNotExist:
                    try:
                        user = User.objects.get(username=username)
                        name = user.first_name + " " + user.last_name
                        profile = Profile.objects.create(user=user, name=name, auto_duty=True, auto_name=True)
                        profile.update()
                        print("Created profile for {}".format(user.username))
                    except:
                        print("Cannot create profile for {}".format(user.username))
