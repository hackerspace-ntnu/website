from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from inventory.models import ItemLoan


def my_scheduled_job():
    

def late_loan_retrieval_poker():
    print("\n\nSending email to late loan retrievals\n")
    loans = ItemLoan.objects.filter(
        loan_to__lt=timezone.now().date(), approver__isnull=False
    )
    for loan in loans:

        print(f"Sending email to {loan.contact_email} about {loan.item}")
        plain_message = render_to_string(
            "inventory/templates/itemloan_late_retrieval_mail.txt",
            {"name": loan.contact_name, "item": loan.item.name},
        )
        send_mail(
            "Påminnelse om tilbakelevering av lånt gjenstand",
            plain_message,
            "Hackerspace NTNU",
            [loan.contact_email],
            fail_silently=False,
        )