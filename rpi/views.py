from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import datetime

from .models import RaspberryPi
from random import choice

names = {
    "ac:7b:a1:56:ae:5a":"Lovelace"
}
availNames = ["Ariel","Jane"]
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
def addrpi(request):
    if request.POST:
        mac = request.POST.get('mac_address','')
        ip = get_client_ip(request)
        hostname = choice(availNames)
        time = datetime.datetime.strftime(datetime.datetime.now(),format="%Y-%m-%d %H:%M")
        RaspberryPi.objects.create(name=hostname,ip=ip,mac=mac,lastSeen=time)
    return HttpResponse(hostname)
def lifesign(request):
    if request.POST:
        mac = request.POST.get('mac_address','')
        ip= get_client_ip(request)
        hostname = names[mac]
        host_rpi = RaspberryPi.objects.filter(mac=mac)
        time = datetime.datetime.strftime(datetime.datetime.now(),format="%Y-%m-%d %H:%M")
        host_rpi.update(name=hostname,ip=ip,mac=mac,lastSeen=time)
    return HttpResponse("Hello, "+hostname)
def detail(request):
    return HttpResponse("Test")

def index(request):
    all_rpis = RaspberryPi.objects.order_by('-lastSeen')[:5]
    template = loader.get_template('rpis.html')
    context = {
        'rpis': all_rpis,
    }
    return HttpResponse(template.render(context, request))
