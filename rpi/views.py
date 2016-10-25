from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import datetime

from os.path import join,dirname,realpath
from .models import RaspberryPi
from random import choice

availNames = []
namefile = join(dirname(realpath(__file__)),"availnames.txt")
def reserveName(name):
    global availNames
    availNames.remove(name)
    with open(namefile,mode="w") as f:
        for n in availNames:
            f.write(n+"\n")
    f.close()
def refresh_rpis():
    global availNames
    """
    with open("RPi.json",mode="r") as f:
        for line in f:
            data+=line
    names = json.loads(data)
    """
    availNames = []
    with open(namefile,mode="r") as f:
        for line in f:
            availNames.append(line.strip())
    f.close()

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
def getPi(mac):
    rpis = RaspberryPi.objects.filter(mac=mac)
    if len(rpis) == 0:
        return None
    else:
        return rpis[0]
def addrpi(request):
    if len(availNames)==0:
        refresh_rpis()
    if request.POST:
        mac = request.POST.get('mac_address','')
        ip = get_client_ip(request)
        hostname = choice(availNames)
        time = datetime.datetime.strftime(datetime.datetime.now(),format="%Y-%m-%d %H:%M")
        if getPi(mac) is None:
            RaspberryPi.objects.create(name=hostname,ip=ip,mac=mac,lastSeen=time)
            reserveName(hostname)
            return HttpResponse(hostname)
        else:
            print("{} already exists".format(mac))
            return HttpResponse("")
def lifesign(request):
    if len(availNames)==0:
        refresh_rpis()
    if request.POST:
        mac = request.POST.get('mac_address','')
        reported_hostname = request.POST.get('hostname','')
        host_rpi = getPi(mac)
        if host_rpi is not None:
            ip= get_client_ip(request)
            time = datetime.datetime.strftime(datetime.datetime.now(),format="%Y-%m-%d %H:%M")
            hostname = host_rpi.name
            if reported_hostname != hostname:
                host_rpi.update(name=hostname)
            host_rpi.update(ip=ip,lastSeen=time)
            return HttpResponse("Hello, "+hostname)
        else:
            return HttpResponse("You're new here, arent'cha?")
    else:
        return HttpResponse("We only serve POST requests here")
def index(request):
    all_rpis = RaspberryPi.objects.order_by('-lastSeen')[:5]
    template = loader.get_template('rpis.html')
    context = {
        'rpis': all_rpis,
    }
    return HttpResponse(template.render(context, request))
