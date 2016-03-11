from django.shortcuts import render
from django.http import HttpResponse
from .models import DoorStatus, OpenData, Point
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
                        door_status_object = DoorStatus(name='hackerspace', datetime=timezone.now, status=status)

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

    try:
        plot_obj = DoorStatus.objects.get(name='plotchart')
    except DoorStatus.DoesNotExist:
        plot_obj = DoorStatus(name='plotchart', status=not door_obj.status, datetime=timezone.now())
        plot_obj.save()

    if (timezone.now() - plot_obj.datetime).total_seconds() > 180 or plot_obj.status != door_obj.status or Point.objects.count() == 0:

        if OpenData.objects.count() == 0 {
            return HttpResponseRedirect("/")
        }

        Point.objects.all().delete()

        start = OpenData.objects.all()[0].opened
        start = start - timedelta(minutes=start.minute % 10, seconds=start.second, microseconds=start.microsecond)
        end = timezone.now()
        end = end - timedelta(minutes=end.minute % 10, seconds=end.second, microseconds=end.microsecond)

        index = 0
        status = 0
        statusAdded = False
        tooltipString = ["Closed", "Open"]
        for seconds in range(0, int((end-start).total_seconds()), 600):
            if index < len(OpenData.objects.all()):
                while (status == 0 and seconds > (OpenData.objects.all()[index].opened-start).total_seconds()) or (status == 1 and seconds > (OpenData.objects.all()[index].closed-start).total_seconds()):
                    if status == 0 and seconds > (OpenData.objects.all()[index].opened-start).total_seconds():
                        entry = Point(datetime=OpenData.objects.all()[index].opened, status=status, tooltip="Door opened " + str(OpenData.objects.all()[index].opened))
                        entry.save()
                        status = 1
                        entry = Point(datetime=OpenData.objects.all()[index].opened, status=status, tooltip="Door opened " + str(OpenData.objects.all()[index].opened))
                        entry.save()
                    if status == 1 and seconds > (OpenData.objects.all()[index].closed-start).total_seconds():
                        entry = Point(datetime=OpenData.objects.all()[index].closed, status=status, tooltip="Door closed " + str(OpenData.objects.all()[index].closed))
                        entry.save()
                        status = 0
                        entry = Point(datetime=OpenData.objects.all()[index].closed, status=status, tooltip="Door closed " + str(OpenData.objects.all()[index].closed))
                        entry.save()
                        index += 1
                        if index >= len(OpenData.objects.all()):
                            break
            if seconds > (door_obj.datetime-start).total_seconds() and not statusAdded:
                statusAdded = True
                if door_obj.status:
                    entry = Point(datetime=door_obj.datetime, status=0, tooltip="Door opened "+str(door_obj.datetime))
                    entry.save()
                    entry = Point(datetime=door_obj.datetime, status=1, tooltip="Door opened "+str(door_obj.datetime))
                    entry.save()
                    status = 1
            entry = Point(datetime=start + timedelta(0, seconds), status=status, tooltip=str(tooltipString[status]))
            entry.save()
        if door_obj.status:
            entry = Point(datetime=timezone.now(), status=1, tooltip="Currently open")
            entry.save()
        else:
            entry = Point(datetime=timezone.now(), status=0, tooltip="Currently closed")
            entry.save()

        plot_obj.datetime = timezone.now()
        plot_obj.status = door_obj.status
        plot_obj.save()

    context = {
        'plot_list': Point.objects.all(),
        'end': timezone.now(),
        'start': timezone.now() - timedelta(0, 43200)
    }
    return render(request, 'chart.html', context)
