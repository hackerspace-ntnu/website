from django import template

from seasonal_events.models import Season

register = template.Library()


@register.tag
def season_data(parser, token):
    return CurrentSeason()


class CurrentSeason(template.Node):
    """
    Denne klassen gir navnet på en tidsbestemt season og en tilhørende
    logo-url til context. Dersom det er overlapp mellom datoer vil
    season med senest startdato prioriteres.

    Om ingen seasons foregår gis standardlogoen og navnet "default".
    """

    def render(self, context):
        # Standard season
        context["logo_url"] = "/static/website/img/logo/hackerspace.svg"
        context["coglight_url"] = "/static/website/img/logo/coglight.svg"
        context["season"] = "default"
        context["disable_reservations"] = None

        for s in Season.objects.filter(active=True).order_by("start_date"):
            if s.is_now():
                # Check if season has a custom logo
                try:
                    context["logo_url"] = s.logo.url
                except ValueError:
                    pass
                context["season"] = s.name
                context["disable_reservations"] = s.disable_reservations

        print(context["season"] + "  " + context["logo_url"])

        return ""
