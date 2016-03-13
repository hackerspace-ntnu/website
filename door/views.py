from django.shortcuts import render
from django.http import HttpResponse
from .models import DoorStatus, OpenData
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from website import settings
from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponseRedirect
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
                        door_status_object = DoorStatus(name='hackerspace', datetime=timezone.now(), status=status)

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

                            currentIndex = openData.id
                            old = OpenData.objects.filter(id__lte = currentIndex - 50)
                            old.delete()

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
    opendata_list = list(reversed(opendata_list))
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

def door_chart(request):
    try:
        door_obj = DoorStatus.objects.get(name='hackerspace')
    except DoorStatus.DoesNotExist:
        door_obj = DoorStatus(name='hackerspace', status=True, datetime=timezone.now())

    s = ""
    for opendata in OpenData.objects.all():
        s += '{"column-1": 0, "date": "'
        s += opendata.opened.strftime('%Y-%m-%d %H:%M:%S')
        s += '"},\n'
        s += '{"column-1": 1, "date": "'
        s += opendata.opened.strftime('%Y-%m-%d %H:%M:%S')
        s += '"},\n'
        s += '{"column-1": 1, "date": "'
        s += opendata.closed.strftime('%Y-%m-%d %H:%M:%S')
        s += '"},\n'
        s += '{"column-1": 0, "date": "'
        s += opendata.closed.strftime('%Y-%m-%d %H:%M:%S')
        s += '"},\n'

    if door_obj.status:
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

    import html.parser
    html_parser = html.parser.HTMLParser()
    s = html_parser.unescape(s)

    context = {
        'open_data': s,
    }
    return render(request, 'chart.html', context)
