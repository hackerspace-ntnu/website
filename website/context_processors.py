import re

from django.http import HttpRequest

from .models import Banner


def template_imports(_: HttpRequest):
    """
    Collection of script tags, stylesheets and other common imports used throughout the site
    Mostly to avoid multiple versions of the same dependency from CDN script tags (looking at you jQuery...)

    Usage:
        '''
        {% block head %}
            ...
            {{ <name-of-import> | safe }}
            ...
        {% endblock %}
        '''

    A more robust solution could be worth it if this list grows further, or better versioning is desired
    """

    return {
        "jquery": """<script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>""",
        "jquery_ui": """<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.min.js" integrity="sha256-VazP97ZCwtekAsvgPBSUwPFKdrwD3unUfSGVYrahUqU=" crossorigin="anonymous"></script>""",
        "materialize_css": """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">""",
        "materialize_js": """<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.js"></script>""",
        "google_fonts": """<link href="https://fonts.googleapis.com/css?family=Montserrat:100,100i,200,200i,300,300i,400,400i,500,500i,600,600i,700,700i,800,800i,900|Open+Sans:300,300i,400,400i,600,600i,700,700i,800,800i" rel="stylesheet">""",
        "google_icons": """<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">""",
        "fullcalendar": """
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fullcalendar/core@4.1.0/main.min.css">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fullcalendar/daygrid@4.1.0/main.min.css">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fullcalendar/timegrid@4.1.0/main.min.css">
        <script src="https://cdn.jsdelivr.net/npm/moment@2.29.1/moment.js"></script>
        <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/@fullcalendar/core@4.1.0/main.min.js"></script>
        <script src='https://cdn.jsdelivr.net/npm/@fullcalendar/moment@4.1.0/main.min.js'></script>
        <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/@fullcalendar/interaction@4.1.0/main.min.js"></script>
        <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/@fullcalendar/daygrid@4.1.0/main.min.js"></script>
        <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/@fullcalendar/timegrid@4.1.0/main.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@fullcalendar/core@4.1.0/locales/nb.js"></script>
        """,
    }


def mazemap_location(_: HttpRequest):
    return {
        "mazemap_link": "https://use.mazemap.com/?v=1&campusid=1&sharepoitype=identifier&sharepoi=360-A2-116"
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
