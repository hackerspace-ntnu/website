import datetime

from django.http import HttpResponse
from django.template import loader

from .models import RaspberryPi


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def add_rpi(request):
    if request.POST:
        mac = request.POST.get("mac_address", "")
        ip = get_client_ip(request)
        hostname = RaspberryPi.suggest_name()
        time = datetime.datetime.now()
        if RaspberryPi.objects.filter(mac=mac).exists():
            return HttpResponse("{} already exists".format(mac), status=400)
        else:
            RaspberryPi.objects.create(name=hostname, ip=ip, mac=mac, last_seen=time)
            return HttpResponse(hostname, status=201)
    else:
        return HttpResponse("We only serve POST requests here", status=405)


def lifesign(request):
    if request.POST:
        mac = request.POST.get("mac_address", "")
        reported_hostname = request.POST.get("hostname", "")
        try:
            host_rpi = RaspberryPi.objects.get(mac=mac)
            ip = get_client_ip(request)
            time = datetime.datetime.now()
            host_rpi.update(ip=ip, last_seen=time, name=reported_hostname)
            return HttpResponse("Hello, " + reported_hostname, status=200)
        except RaspberryPi.DoesNotExist:
            return HttpResponse("You're new here, arent'cha?", status=400)
    else:
        return HttpResponse("We only serve POST requests here", status=405)


def index(request):
    all_rpis = RaspberryPi.objects.order_by("-last_seen")[:5]
    template = loader.get_template("rpis.html")
    context = {
        "rpis": all_rpis,
    }
    return HttpResponse(template.render(context, request))
