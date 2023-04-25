from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_phone_number(number):
    number = number.replace(" ", "")
    has_areacode = number[0] == "+" or number[:2] == "00"

    if len(number) == 8 and number.isdigit():
        return
    if has_areacode and number[1:].isdigit():
        return

    raise ValidationError(
        _(
            "Nummeret må være 8 siffer eller starte med landskode på formen +47 eller 0047"
        )
    )
