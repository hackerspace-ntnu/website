import os
import json
import requests

from django.http import JsonResponse
#TODO: Gjøre unpack som tupler i stedet
def hent_vaktliste():
    """
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    vaktliste = os.path.join(cur_dir, "vaktliste.json")
    with open(vaktliste,"r") as f:
        return json.loads(f.read())
    """
    return requests.get("https://script.googleusercontent.com/macros/echo?user_content_key=gR05slZZQrkrumxUc8DJZEc81FUEXWJpVDu8OGmYc7Bd8STD9BEvHnNLn3Hqa93sZAkXhzOJJfVsxRBCis22hxj50ZyEv7V0m5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnBHVJ4Ip7UlCqkboOF3idyLswydE_Rh_IZ2xA43kME624RrB2b1T6_LZIUQtyudpTtsAUXIaJqQ5&lib=MvQgEbo5GAfi_xTmCXLhSAK0T_1fexhuo").json()

def vakt_filter(dager,tider):
    filter_data = {}
    filter_times = []
    filter_days = [d.title() for d in dager if d!='']
    for tid in tider:
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
    for day in vakt_data:    
        if len(filter_days)==0 or day in filter_days: # Dagen slipper gjennom filteret
            if len(filter_times)==0: # what is time
                filter_data[day] = vakt_data[day]
            else:
                vakter = {}
                for time_slot in vakt_data[day]:
                    if time_slot in filter_times: # Vakttiden slipper gjennom filteret
                        vakter[time_slot] = vakt_data[day][time_slot]
                filter_data[day] = vakter

    return filter_data

def finn_person(person,full=True):
    filter_data = {}
    vakt_data = hent_vaktliste()
    for day in vakt_data:
        for time in vakt_data[day]:
            for hacker in [p.lower() for p in vakt_data[day][time]]:
                if person.lower() in hacker: #TODO: Gjøre dette til fuzzy finding
                    if full:
                        if day in filter_data:
                            filter_data[day][time]=vakt_data[day][time]
                        else:
                            filter_data[day] = {time: vakt_data[day][time]}
                    else:
                        if day in filter_data:
                            filter_data[day][time]=[hacker.title()]
                        else:
                            filter_data[day] = {time: [hacker.title()]}
                    break
    if len(filter_data)==0:
        return {}
    else:
        return filter_data

def vakter(request):
    dager = request.GET.get('dag','')
    tider = request.GET.get('tid','')
    vakt_data = vakt_filter(dager.split(","),tider.split(","))
    return JsonResponse(vakt_data)

def personsok(request):
    person = request.GET.get('person','')
    if person=='': person="FACK"
    full = request.GET.get('full','')
    if full in ['', 'True']:
        full = True
    elif full=="False":
        full = False
    vakt_data = finn_person(person,full=full)
    return JsonResponse(vakt_data)
