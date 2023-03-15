from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib

from inventory.models import ItemLoan


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


def amogus():
    # Create message object instance
    msg = MIMEMultipart()

    # Define email parameters
    sender_email = settings.DEFAULT_FROM_MAIL
    recipient_email = "alexamol@stud.ntnu.no"
    subject = "Du har vært litt for sussy!"

    # Attach the image to the email
    with open('static/img/misc/easteregg.png', 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-Disposition', 'attachment', filename="cat_picture.jpg")
        msg.attach(img)

    # Define message headers
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Define SMTP server details and login credentials
    smtp_server = settings.EMAIL_HOST
    smtp_port = settings.EMAIL_PORT
    smtp_username = 'hacker_space@yahoo.com'
    smtp_password = 'QckNmieE6Lahhcm'

    # Create a SMTP session and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())