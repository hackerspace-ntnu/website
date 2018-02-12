import json
from datetime import datetime

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from website import settings
from .models import CoffeePot, OpenData
import html.parser

@csrf_exempt
def coffee_pot(request):
    if request.method == 'POST':

        # Decode data
        unico = request.body.decode('utf-8')
        data = json.loads(unico)
        print(data)

        # Authenticate message
        if 'key' in data and 'pot' in data:
            if data['key'] == settings.DOOR_KEY:
                coffee_status_object = CoffeePot.get_coffee_by_name(data['pot'])

                # Coffee brewed
                coffee_status_object.datetime = timezone.now()
                coffee_status_object.save()
    return HttpResponse(" ")


def get_json(request):
    coffee_json = {}
    for pot in CoffeePot.objects.all():
        try:
            coffee_json[pot.name]=pot.datetime.strftime("%a %b %d %H:%M:%S")
        except AttributeError:
            coffee_json[pot.name]=""
    return JsonResponse(coffee_json)

@csrf_exempt
def get_coffee(request,pot):
    coffee = CoffeePot.get_coffee_by_name(pot)
    last_changed = str(coffee.datetime)
    return HttpResponse(last_changed)


def coffee_data(request):
    open_coffee_list = OpenData.objects.all()
    open_coffee_list = list(reversed(open_coffee_list))
    for data in open_coffee_list:
        data.deltaTime = data.closed - data.opened
    status = CoffeePot.get_coffee_by_name(COFFEE_NAME)

    context = {
        'open_data_list': open_coffee_list,
        'status': status,
    }

    return render(request, 'coffee_data.html', context)


def coffee_chart(request):
    coffee_obj = CoffeePot.get_coffee_by_name(COFFEE_NAME)

    s = ""

    # Plot graphs for all open periods (OpenDatas)
    for open_data in OpenData.objects.all():
        s += '{"column-1": 0, "date": "'
        s += open_data.opened.strftime('%Y-%m-%d %H:%M:%S')
        s += '"},\n'
        s += '{"column-1": 1, "date": "'
        s += open_data.opened.strftime('%Y-%m-%d %H:%M:%S')
        s += '"},\n'
        s += '{"column-1": 1, "date": "'
        s += open_data.closed.strftime('%Y-%m-%d %H:%M:%S')
        s += '"},\n'
        s += '{"column-1": 0, "date": "'
        s += open_data.closed.strftime('%Y-%m-%d %H:%M:%S')
        s += '"},\n'

    # Plot current status
    if coffee_obj.status:
        s += '{"column-1": 0, "date": "'
        s += door_obj.datetime.strftime('%Y-%m-%d %H:%M:%S')
        s += '"},\n'
        s += '{"column-1": 1, "date": "'
        s += door_obj.datetime.strftime('%Y-%m-%d %H:%M:%S')
        s += '"},\n'
        s += '{"column-1": 1, "date": "'
        s += timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        s += '"},\n'
    else:
        s += '{"column-1": 0, "date": "'
        s += timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        s += '"},\n'

    html_parser = html.parser.HTMLParser()
    s = html_parser.unescape(s)

    context = {
        'open_data': s,
    }

    return render(request, 'chart.html', context)
