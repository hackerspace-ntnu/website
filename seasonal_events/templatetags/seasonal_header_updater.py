from django import template
from seasonal_events.models import Season
register = template.Library()


@register.tag
def season_data(parser,token):
    return CurrentSeason()


class CurrentSeason(template.Node):

    def render(self, context):
        context["logo_url"] = "/website/img/logo/Hackerspace_huge.png"
        context["season"] = "default"
        for s in Season.objects.filter(active=True):
            if s.isNow():
                context["logo_url"] = "seasonal_events/seasonal_logos/"+s.header_name+".png"
                context["season"] = s.name
        print(context["season"]+"  "+context["logo_url"])

        return ''
