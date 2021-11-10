import html.parser
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from website import settings

from .models import DoorStatus, OpenData

DOOR_NAME = "hackerspace"


class DoorView(View):
    def get(self, request):
        return HttpResponse(DoorStatus.get_door_by_name(DOOR_NAME).status)

    def post(self, request):
        # Decode data
        unico = request.body.decode("utf-8")
        data = json.loads(unico)

        # Authenticate message
        if "key" in data and "status" in data:
            if data["key"] == settings.DOOR_KEY:
                status = data["status"]
                door_status_object = DoorStatus.get_door_by_name(DOOR_NAME)

                # Door open
                if status is True and door_status_object.status is False:
                    # Save status and time to door status object
                    door_status_object.status = status
                    door_status_object.datetime = timezone.now()
                    door_status_object.save()

                # Door closed
                elif status is False and door_status_object.status is True:
                    # Create OpenData object with open and close datetime
                    open_data = OpenData(
                        opened=door_status_object.datetime, closed=timezone.now()
                    )
                    open_data.save()

                    # Save status and time to door status object
                    door_status_object.status = status
                    door_status_object.datetime = timezone.now()
                    door_status_object.save()

                    # Limit amount of OpenData objects to 50
                    current_index = open_data.id
                    old = OpenData.objects.filter(id__lte=current_index - 50)
                    old.delete()
        return HttpResponse(" ")


class DoorJsonView(View):
    def get(self, request):
        door = DoorStatus.get_door_by_name(DOOR_NAME)
        status = door.status
        last_changed = str(door.datetime)

        data = {"status": status, "lastChanged": last_changed}
        return JsonResponse(data)
