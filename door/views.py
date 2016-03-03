from django.shortcuts import render
from django.http import HttpResponse
from .models import DoorStatus, OpenData
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from website import settings
from datetime import datetime
from django.http import JsonResponse
import json

# Create your views here.

@csrf_exempt
def door_post(request):
    if request.method == 'POST':
        unico = request.body.decode('utf-8')
        data = json.loads(unico)
        if 'key' in data:
            if data['key'] == settings.DOOR_KEY:
                if 'status' in data:
                    status = data['status']

                    try:
                        door_status_object = DoorStatus.objects.get(name='hackerspace')
                    except DoorStatus.DoesNotExist:
                        door_status_object = DoorStatus(name='hackerspace')

                    if status == True:
                        door_status_object.status = status
                        door_status_object.save()
                        if 'timeStart' in data and 'dateStart' in data:
                            timeStart = data['timeStart']
                            dateStart = data['dateStart']
                            opened = datetime.strptime(dateStart+"."+timeStart,"%Y-%m-%d.%H:%M:%S")
                            door_status_object.datetime = opened
                            door_status_object.save()
                    elif status == False:
                        door_status_object.status = status
                        door_status_object.save()
                        if 'timeStart' in data and 'dateStart' in data and 'timeEnd' in data and 'dateEnd' in data:
                            timeStart = data['timeStart']
                            dateStart = data['dateStart']
                            timeEnd = data['timeEnd']
                            dateEnd = data['dateEnd']
                            opened = datetime.strptime(dateStart+"."+timeStart,"%Y-%m-%d.%H:%M:%S")
                            closed = datetime.strptime(dateEnd+"."+timeEnd,"%Y-%m-%d.%H:%M:%S")
                            openData = OpenData(opened=opened, closed=closed)
                            openData.save()

                            door_status_object.datetime = closed
                            door_status_object.save()
    return HttpResponse(" ")

@csrf_exempt
def get_status(request):
    try:
        status = DoorStatus.objects.get(name='hackerspace').status
    except DoorStatus.DoesNotExist:
        status = True
    return HttpResponse(status)

def get_json(request):
    try:
        status = DoorStatus.objects.get(name='hackerspace').status
        lastChanged = str(DoorStatus.objects.get(name='hackerspace').datetime)
    except DoorStatus.DoesNotExist:
        status = True
        lastChanged = 'error'
    data = {}
    data['status'] = status
    data['lastChanged'] = lastChanged
    return JsonResponse(data)

def door_data(request):
    opendata_list = OpenData.objects.all()
    for data in opendata_list:
        data.deltaTime = data.closed - data.opened
    try:
        status = DoorStatus.objects.get(name='hackerspace')
    except DoorStatus.DoesNotExist:
        status = DoorStatus(name='hackerspace')
    context = {
        'opendata_list': opendata_list,
        'status': status,
    }

    return render(request, 'door_data.html', context)
