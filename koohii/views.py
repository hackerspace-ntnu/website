import json
from datetime import datetime,timedelta

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from website import settings
from .models import CoffeePot, CoffeeData
import html.parser

@csrf_exempt
def coffee_pot(request):
    if request.method == 'POST':

        # Decode data
        unico = request.body.decode('utf-8')
        data = json.loads(unico)

        # Authenticate message
        if 'key' in data and 'pot' in data:
            if data['key'] == settings.DOOR_KEY:
                coffee_status_object = CoffeePot.get_coffee_by_name(data['pot'])

                # Coffee brewed
                open_data=CoffeeData(brewed=timezone.now(),pot=data['pot'])
                open_data.save()
                coffee_status_object.datetime = timezone.now()
                coffee_status_object.save()
                return HttpResponse("Thanks for filling me up ;)\n-{}\n".format(data['pot']))
            else:
                return HttpResponse("Wrong key :C\n")
        else:
            return HttpResponse("Malformed request\n")

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
    coffee_data_list = CoffeeData.objects.all()
    coffee_data_list = list(reversed(coffee_data_list))

    context = {
        'coffee_data_list': open_coffee_list,
    }

    return render(request, 'coffee_data.html', context)


def coffee_chart(request):
    finn = ""
    mathias = ""

    for coffee_data in CoffeeData.objects.all():
        if coffee_data.pot == "Finn":
            finn += '{"column-1": 0, "date": "'
            finn += coffee_data.brewed.strftime('%Y-%m-%d %H:%M:%S')
            finn += '","name": "'
            finn += coffee_data.pot
            finn += '"},\n'
            finn += '{"column-1": 1, "date": "'
            finn += coffee_data.brewed.strftime('%Y-%m-%d %H:%M:%S')
            finn += '","name": "'
            finn += coffee_data.pot
            finn += '"},\n'
            finn += '{"column-1": 1, "date": "'
            finn += (coffee_data.brewed+timedelta(seconds=10)).strftime('%Y-%m-%d %H:%M:%S')
            finn += '","name": "'
            finn += coffee_data.pot
            finn += '"},\n'
            finn += '{"column-1": 0, "date": "'
            finn += (coffee_data.brewed+timedelta(seconds=10)).strftime('%Y-%m-%d %H:%M:%S')
            finn += '","name": "'
            finn += coffee_data.pot
            finn += '"},\n'
        elif coffee_data.pot == "Mathias":
            mathias += '{"column-1": 0, "date": "'
            mathias += coffee_data.brewed.strftime('%Y-%m-%d %H:%M:%S')
            mathias += '","name": "'
            mathias += coffee_data.pot
            mathias += '"},\n'
            mathias += '{"column-1": 1, "date": "'
            mathias += coffee_data.brewed.strftime('%Y-%m-%d %H:%M:%S')
            mathias += '","name": "'
            mathias += coffee_data.pot
            mathias += '"},\n'
            mathias += '{"column-1": 1, "date": "'
            mathias += (coffee_data.brewed+timedelta(seconds=10)).strftime('%Y-%m-%d %H:%M:%S')
            mathias += '","name": "'
            mathias += coffee_data.pot
            mathias += '"},\n'
            mathias += '{"column-1": 0, "date": "'
            mathias += (coffee_data.brewed+timedelta(seconds=10)).strftime('%Y-%m-%d %H:%M:%S')
            mathias += '","name": "'
            mathias += coffee_data.pot
            mathias += '"},\n'


    finn += '{"column-1": 0, "date": "'
    finn += timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    finn += '"},\n'
    finn += '{"column-1": 0, "date": "'
    finn += timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    finn += '"},\n'
    
    mathias += '{"column-1": 0, "date": "'
    mathias += timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    mathias += '"},\n'
    mathias += '{"column-1": 0, "date": "'
    mathias += timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    mathias += '"},\n'


    html_parser = html.parser.HTMLParser()
    finn = html_parser.unescape(finn)
    mathias = html_parser.unescape(mathias)

    context = {
        'coffee_data_finn': finn,
        'coffee_data_mathias': mathias,
    }

    return render(request, 'coffee_chart.html', context)
