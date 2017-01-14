from django.core.management.base import BaseCommand
from django.core.mail import send_mass_mail
from applications.models import ProjectApplication


class Command(BaseCommand):
    help = "Sends email to every person who has registered to be notified when the" \
           "project group applications open."

    def handle(self, *args, **options):
        emails = ProjectApplication.objects.all()

        subject = "Opptaket til Hackerspace sin prosjektgruppe har åpnet"
        content = "Test"
        from_address = "web.hackerspace.ntnu@gmail.com"

        send_mass_mail([(subject, content, from_address, [email]) for email in emails])
