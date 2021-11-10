import re

from .models import Banner


def common_info(request):
    return {
        "mazemap_link": "https://use.mazemap.com/?v=1&campusid=1&sharepoitype=identifier&sharepoi=360-A2-116",
    }


def banner_context(request):
    banners = []
    for banner in Banner.objects.all():
        if not banner.is_active():
            continue

        # Match against the site patterns
        should_show = False
        for site in banner.site.split(","):
            site_pattern = re.compile(site.replace("*", ".*"))
            if site_pattern.match(request.resolver_match.view_name):
                should_show = True
                break

        if should_show:
            color = banner.color
            if color == "hs-green":
                color = "#5bba47"
            elif color == "hs-yellow":
                color = "#f6be00"
            elif color == "hs-red":
                color = "#e25e48"

            text_color = banner.text_color
            if text_color == "hs-black":
                text_color = "#000000"
            elif text_color == "hs-white":
                text_color = "#ffffff"

            banners.append(
                {"text": banner.text, "color": color, "text_color": text_color}
            )

    return {"banners": banners}
