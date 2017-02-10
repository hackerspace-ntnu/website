import datetime

from django.conf import settings
from django.http.response import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.views.generic.list import ListView

from .models import RaspberryPi


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    else:
        return request.META.get('REMOTE_ADDR')


class RPiListView(ListView):
    model = RaspberryPi
    ordering = ('-last_seen',)
    template_name = 'rpis.html'
    context_object_name = 'rpis'


class RPiAPIView(View):
    def get(self, request, **kwargs):
        return JsonResponse(
            data={
                'pis': [
                    {
                        'name': pi.name,
                        'mac': pi.mac,
                        'ip': pi.ip,
                        'last_seen': pi.last_seen.isoformat()
                    } for pi in RaspberryPi.objects.all()
                    ]
            }
        )

    @csrf_exempt
    def post(self, request, **kwargs):
        key = request.POST.get('secret_key')

        if not key:
            return HttpResponseBadRequest('secret_key not provided.', status=401)

        if not key == getattr(settings, 'RPI_SECRET_KEY'):
            return HttpResponseBadRequest('secret_key not valid.', status=401)

        mac = request.POST.get('mac_address')
        ip = get_client_ip(request)
        time = datetime.datetime.now()

        is_new = False
        try:
            pi = RaspberryPi.objects.get(mac=mac)
        except RaspberryPi.DoesNotExist:
            is_new = True
            pi = RaspberryPi(
                mac=mac,
                name=RaspberryPi.suggest_name(),
            )

        pi.ip = ip
        pi.last_seen = time

        pi.full_clean()
        pi.save()

        return JsonResponse(
            data={
                'name': pi.name,
                'mac': pi.mac,
                'ip': pi.ip,
                'last_seen': pi.last_seen,
            },
            status=201 if is_new else 200
        )
