from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import RaspberryPi
from random import choice

names = {
    "ac:7b:a1:56:ae:5a":"Lovelace"
}
availNames = ["Ariel","Jane"]
def add(request):
    if request.POST:
        mac = request.POST.get('mac_address','')
    return choice(availNames)
def dontdieonme(request):
    mac = ""
    if request.POST:
        mac = request.POST.get('mac_address','')
    return "Hello,"+names[mac]
def detail(request):
    return HttpResponse("Test")

def index(request):
    all_rpis = RaspberryPi.objects.order_by('-lastSeen')[:5]
    template = loader.get_template('rpis.html')
    context = {
        'rpis': all_rpis,
    }
    return HttpResponse(template.render(context, request))
