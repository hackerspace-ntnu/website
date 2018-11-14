from internal.models import TimeTable


class TermConverter:
    regex = "[0-9]{2}[VH]"

    def to_python(self, value):
        try:
            TimeTable.objects.get(term=value)
        except TimeTable.DoesNotExist:
            raise ValueError
        return value

    def to_url(self, value):
        return value
