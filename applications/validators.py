from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_phone_number(number):
    has_areacode = number[0] == "+" or number[:1] == "00"
    if len(number) != 8 and (not has_areacode or number[1:].isdigit()):
        raise ValidationError(
            _(
                "Nummeret må være 8 siffer eller starte med landskode på formen +47 eller 0047"
            )
        )
    if len(number) == 8 and not number.isdigit():
        raise ValidationError(_("Nummeret må være 8 siffer"))
