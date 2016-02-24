from django.shortcuts import render
from django.http import HttpResponse
from .models import DoorStatus
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def update_door_status(request):
    if request.method == 'POST':
        door_status_object = DoorStatus.objects.get(name='hs')
        status = request.POST.get('status','')
        if status == '0':
            #print('DOOR IS CLOSED')
            door_status_object.status = False
        elif status == '1':
            door_status_object.status = True
            #print('DOOR IS OPEN')
        door_status_object.save()
    return HttpResponse(" ")
