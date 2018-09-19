import datetime
import requests
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

cache_time = "Never"
vakt_cache_tuples = ""
vakt_cache_json = ""


def hent_vaktliste(output="json", force_update=False):
    global vakt_cache_tuples, vakt_cache_json, cache_time
    if force_update or not vakt_cache_json or datetime.datetime.now() - cache_time >= datetime.timedelta(
        hours=12):
        vakt_data_json = requests.get(
            "https://script.googleusercontent.com/macros/echo?user_content_key=gR05slZZQrkrumxUc8DJZEc81FUEXWJpVDu8OGmYc7Bd8STD9BEvHnNLn3Hqa93sZAkXhzOJJfVsxRBCis22hxj50ZyEv7V0m5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnBHVJ4Ip7UlCqkboOF3idyLswydE_Rh_IZ2xA43kME624RrB2b1T6_LZIUQtyudpTtsAUXIaJqQ5&lib=MvQgEbo5GAfi_xTmCXLhSAK0T_1fexhuo").json()

        vakt_data_tuples = []
        for day in vakt_data_json:
            for time in vakt_data_json[day]:
                vakt_data_tuples.append((day, time, vakt_data_json[day][time]))

        cache_time = datetime.datetime.now()
        vakt_cache_tuples = vakt_data_tuples
        vakt_cache_json = vakt_data_json

    if output == "tuples":
        return vakt_cache_tuples
    else:
        return vakt_cache_json


def filter_vakt_data(filter_days, filter_times, filter_persons):
    for vakt in hent_vaktliste(output="tuples"):
        if filter_days and vakt[0] not in filter_days and vakt[0][:3] not in filter_days:
            continue
        if filter_times and vakt[1] not in filter_times:
            continue
        if filter_persons and all(
            person_filter not in "".join(vakt[2]).lower() for person_filter in filter_persons):
            continue
        yield vakt


def get_time_slots(times):
    filter_times = []
    time_slots = ["10:15 - 12:07", "12:07 - 14:07", "14:07 - 16:07", "16:07 - 18:00"]
    for time in times.split(","):
        if time:
            time = time.replace(".", ":")
            if ":" not in time:
                time += ":0"

            h, m = map(int, time.split(":"))

            filter_times.append(
                min(time_slots, key=lambda x: abs(time_slots.index(x) * 2 + 11.11 - h - m / 60)))

    return filter_times


def filter_current():
    days = ["Søndag", "Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag"]
    day, time = datetime.datetime.strftime(datetime.datetime.now(), "%w,%H:%M").split(",")
    return vakt_filter(days=days[int(day)], times=time)


def vakt_filter(days="", times="", persons="", full=True, compact=False, output="json"):
    filter_times = get_time_slots(times)
    if output == "tuples":
        filter_data = []
    else:
        filter_data = {}
    filter_days = [d.title() for d in days.split(",") if d]
    filter_persons = [p.lower() for p in persons.split(",") if p]

    for day, time_slot, hackers in filter_vakt_data(filter_days, filter_times, filter_persons):
        if compact:
            day = day[:3]
            time_slot = "".join(time_slot.split(" "))
        if day not in filter_data and output != "tuples":
            filter_data[day] = {}
        if full:
            if output == "tuples":
                filter_data.append((day, time_slot, hackers))
            else:
                filter_data[day][time_slot] = hackers
        else:
            hacker_list = []
            for hacker in {pm for pm in hackers for pf in filter_persons if pf in pm.lower()}:
                if output == "tuples":
                    hacker_list.append({hacker: {}})
                if time_slot not in filter_data[day]:
                    filter_data[day][time_slot] = {}
                filter_data[day][time_slot][hacker] = hackers[hacker]
            if output == "tuples":
                filter_data.append((day, time_slot, hacker_list))

    return filter_data


def vakter(request):
    dager = request.GET.get('dag', '')
    tider = request.GET.get('tid', '')
    personer = request.GET.get('person', '')
    full = request.GET.get('full', '').lower() != "false"
    compact = request.GET.get('compact', '').lower() == "true"
    vakt_data = vakt_filter(days=dager, times=tider, persons=personer, full=full, compact=compact)
    return JsonResponse(vakt_data)


def current(_):
    return JsonResponse(filter_current())


def update(_):
    hent_vaktliste(force_update=True)
    return JsonResponse({"Cache time": cache_time})


def index(request):
    dager = request.GET.get('dag', '')
    tider = request.GET.get('tid', '')
    personer = request.GET.get('person', '')
    full = request.GET.get('full', '').lower() != "on"

    user_list = []
    if any([dager, tider, personer]):
        vakt_data = vakt_filter(days=dager, times=tider, persons=personer, full=full)
        for day in vakt_data:
            for time in vakt_data[day]:
                for name in vakt_data[day][time]:
                    try:
                        name = name.split()
                        user = User.objects.get(first_name__icontains=name[0])
                        user_list.append(user)
                    except:
                        user_list.append(" ".join(name))

    context = {
        "users": user_list
    }
    return render(request, 'vaktliste/vakt_filter.html', context)
