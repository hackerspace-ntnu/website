from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_phone_number(number):
    if len(number) != 8 or not number.isdigit():
        raise ValidationError(_("Nummeret må være 8 siffer"))
