import json
from datetime import datetime

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from website import settings
from .models import DoorStatus, OpenData
import html.parser

DOOR_NAME = "hackerspace"


@csrf_exempt
def door_post(request):
    if request.method == 'POST':

        # Decode data
        unico = request.body.decode('utf-8')
        data = json.loads(unico)

        # Authenticate message
        if 'key' in data:
            if data['key'] == settings.DOOR_KEY:

                if 'status' in data:
                    status = data['status']
                    door_status_object = DoorStatus.get_door_by_name(DOOR_NAME)

                    # Door open
                    if status is True:
                        # Save status to door status object
                        door_status_object.status = status
                        door_status_object.save()

                        # Save datetime to door status object
                        if 'timeStart' in data and 'dateStart' in data:
                            time_start = data['timeStart']
                            date_start = data['dateStart']
                            opened = datetime.strptime(date_start + "." + time_start, "%Y-%m-%d.%H:%M:%S")
                            door_status_object.datetime = opened
                            door_status_object.save()

                    # Door closed
                    elif status is False:
                        # Save status to door status object
                        door_status_object.status = status
                        door_status_object.save()

                        if 'timeStart' in data and 'dateStart' in data and 'timeEnd' in data and 'dateEnd' in data:
                            time_start = data['timeStart']
                            date_start = data['dateStart']
                            time_end = data['timeEnd']
                            date_end = data['dateEnd']
                            opened = datetime.strptime(date_start + "." + time_start, "%Y-%m-%d.%H:%M:%S")
                            closed = datetime.strptime(date_end + "." + time_end, "%Y-%m-%d.%H:%M:%S")

                            # Create OpenData object with open and close datetime
                            open_data = OpenData(opened=opened, closed=closed)
                            open_data.save()

                            # Limit amount of OpenData objects to 50
                            current_index = open_data.id
                            old = OpenData.objects.filter(id__lte=current_index - 50)
                            old.delete()

                            # Save datetime to door status object
                            door_status_object.datetime = closed
                            door_status_object.save()
    return HttpResponse(" ")


@csrf_exempt
def get_status(request):
    return HttpResponse(DoorStatus.get_door_by_name(DOOR_NAME).status)


def get_json(request):
    door = DoorStatus.get_door_by_name(DOOR_NAME)
    status = door.status
    last_changed = str(door.datetime)

    data = {'status': status,
            'lastChanged': last_changed}
    return JsonResponse(data)


def door_data(request):
    open_data_list = OpenData.objects.all()
    open_data_list = list(reversed(open_data_list))
    for data in open_data_list:
        data.deltaTime = data.closed - data.opened
    status = DoorStatus.get_door_by_name(DOOR_NAME)

    context = {
        'open_data_list': open_data_list,
        'status': status,
    }

    return render(request, 'door_data.html', context)


def door_chart(request):
    door_obj = DoorStatus.get_door_by_name(DOOR_NAME)

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

    html_parser = html.parser.HTMLParser()
    s = html_parser.unescape(s)

    context = {
        'open_data': s,
    }

    return render(request, 'chart.html', context)
