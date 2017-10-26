import os
import json
import requests
import json

from django.http import JsonResponse
def hent_vaktliste():
    """
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    vaktliste = os.path.join(cur_dir, "vaktliste.json")
    with open(vaktliste,"r") as f:
        return json.loads(f.read())
    """
    vakt_data = requests.get("https://script.googleusercontent.com/macros/echo?user_content_key=gR05slZZQrkrumxUc8DJZEc81FUEXWJpVDu8OGmYc7Bd8STD9BEvHnNLn3Hqa93sZAkXhzOJJfVsxRBCis22hxj50ZyEv7V0m5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnBHVJ4Ip7UlCqkboOF3idyLswydE_Rh_IZ2xA43kME624RrB2b1T6_LZIUQtyudpTtsAUXIaJqQ5&lib=MvQgEbo5GAfi_xTmCXLhSAK0T_1fexhuo").json()
    vakt_data_tuples = []
    for day in vakt_data:
        for time in vakt_data[day]:
            vakt_data_tuples.append((day,time,vakt_data[day][time]))
    return vakt_data_tuples

def vakt_filter(dager,tider):
    filter_data = {}
    filter_times = []
    filter_days = [d.title() for d in dager.split(",") if d!='']
    for tid in tider.split(","):
        #HERE BE DRAGONS
        if tid!='':
            time_slots = ["10:15 - 12:07","12:07 - 14:07", "14:07 - 16:07", "16:07 - 18:00"]
            h,m = map(int,tid.split(":"))
            timeslot = ""
            #WHY ARE YOU STILL HERE
            if h>=18:
                filter_times.append("16:07 - 18:00")
            elif h<10:
                filter_times.append("10:15 - 12:07")
            else:
                for t in range(10,18,2):
                    if h in range(t,t+2):
                        #AAAAAAAAAAAAAAAAAAAAH
                        if h==t and m<7:
                            filter_times.append(time_slots[max(0,(t-10)//2-1)])
                        else:
                            filter_times.append(time_slots[(t-10)//2])
        #THE DRAGONS ARE GONE
    vakt_data = hent_vaktliste() 
    for vakt in [v for v in vakt_data if (v[0] in filter_days or len(filter_days)==0) and (v[1] in filter_times or len(filter_times)==0)]:
        day = vakt[0]
        time_slot = vakt[1]
        hackers = vakt[2]
        if day not in filter_data:
            filter_data[day] = {}
        filter_data[day][time_slot] = hackers

    return filter_data

def finn_person(persons,full=True):
    filter_data = {}
    vakt_data = hent_vaktliste()
    for person in persons.split(","):
        for vakt in vakt_data:
            day = vakt[0]
            time_slot = vakt[1]
            hackers = vakt[2]
            for hacker in hackers:
                if person.lower() in hacker.lower():
                    if full:
                        if day not in filter_data:
                            filter_data[day] = {}
                        filter_data[day][time_slot] = hackers
                    else:
                        if day not in filter_data:
                            filter_data[day] = {}
                        filter_data[day][time_slot] = [hacker]
                    break
    if len(filter_data)==0:
        return {}
    else:
        return filter_data

def vakter(request):
    dager = request.GET.get('dag','')
    tider = request.GET.get('tid','')
    vakt_data = vakt_filter(dager,tider)
    return JsonResponse(vakt_data)

def personsok(request):
    person = request.GET.get('person','FACK')
    full = request.GET.get('full','')
    if full in ['', 'True']:
        full = True
    elif full=="False":
        full = False
    vakt_data = finn_person(person,full=full)
    return JsonResponse(vakt_data)
