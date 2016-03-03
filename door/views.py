from django.shortcuts import render
from django.http import HttpResponse
from .models import DoorStatus
from django.views.decorators.csrf import csrf_exempt
from website import settings
import json

# Create your views here.

@csrf_exempt
def door_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if 'key' in data:
            if data['key'] == settings.DOOR_KEY:
                if 'status' in data:
                    status = data['status']
                    if DoorStatus.objects.filter(name='hackerspace').count():
                        door_status_object = DoorStatus.objects.get(name='hackerspace')
                    else:
                        door_status_object = DoorStatus(name='hackerspace')
                    door_status_object.status = status
                    door_status_object.save()
                    #print("STATUS:", status)
                if 'date' in data:
                    date = data['date']
                    #print("DATE:", date)
                if 'time' in data:
                    time = data['time']
                    #print("TIME:", time)

    return HttpResponse(" ")
