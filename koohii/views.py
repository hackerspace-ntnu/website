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
                return HttpResponse("Thanks for filling me up ;)\n-{}\n".format(data['pot']),status=201)
            else:
                return HttpResponse("Wrong key :C\n",status=451)
        else:
            return HttpResponse("Malformed request\n",status=418)

def get_json(request):
    coffee_json = {}
    for pot in CoffeePot.objects.all():
        coffee_json[pot.name]=pot.datetime.strftime("%a %b %d %H:%M")
    return JsonResponse(coffee_json)

@csrf_exempt
def get_coffee(request,pot):
    coffee = CoffeePot.get_coffee_by_name(pot)
    last_changed = str(coffee.datetime.strftime("%a %b %d %H:%M"))
    return HttpResponse(last_changed)


def coffee_data(request):
    finn = CoffeePot.get_coffee_by_name("Finn")
    mathias = CoffeePot.get_coffee_by_name("Mathias")
    coffee_data_list = list(CoffeeData.objects.order_by('-brewed'))

    context = {
        'coffee_data_list': coffee_data_list,
        'finn': finn,
        'mathias': mathias
    }

    return render(request, 'coffee_data.html', context)


def coffee_chart(request):
    coffee_data_list = []

    for coffee_data in CoffeeData.objects.order_by('brewed'):
        name = coffee_data.pot
        time_brewed = coffee_data.brewed.strftime('%Y-%m-%d %H:%M')
        coffee_data_list.append({"column-1":1, "date": time_brewed,"name": name})

    coffee_data_list.append({"column-1":0, "date": datetime.now().strftime('%Y-%m-%d %H:%M'),"name": "Nå"})


    context = {
            'coffee_data': json.dumps(coffee_data_list)[1:-1]
    }

    return render(request, 'coffee_chart.html', context)
