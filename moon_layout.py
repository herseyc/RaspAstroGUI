from tkinter import *
from get_gps import *
from raspastroinfo import AstroData
import time
import math
from rasp_calc_func import *
from datetime import datetime, timedelta, timezone

root = Tk()
root.title("Moon")
root.config(bg="black")

def handle_button_press():
    root.destroy()

def now_time():
    utc_now = datetime.utcnow()
    return utc_now

# Moon Current Frame
moon_frame = Frame(root, width=400)
moon_frame.grid(row=0, column=0, padx=10, pady=5)

# Moon Data Frame
moondata_frame = Frame(root, width=400)
moondata_frame.grid(row=1, column=0, padx=10, pady=5)
numdays = 15
Label(moondata_frame, text="15 Days of Moon", font='Arial 12 bold').grid(row=0, columnspan=4, padx=5, pady=5)
Label(moondata_frame, text="Day").grid(row=1, column=0, padx=2, pady=2)
Label(moondata_frame, text="Rise").grid(row=1, column=1, padx=2, pady=2)
Label(moondata_frame, text="Set").grid(row=1, column=2, padx=2, pady=2)
Label(moondata_frame, text="Phase at Rise").grid(row=1, column=3, padx=2, pady=2)


# Button Frame
bottom = Frame(root)
bottom.grid(column=0, padx=10, pady=5)


gps_data_tuple = get_gps_data()
gps_data = gps_data_tuple[6]

astro = {}
astro = AstroData(obslat=gps_data[1], obslon=gps_data[2], obslev=gps_data[3], obshorizon="-0:34", obsepoch=now_time())
astro.obs.pressure = 0

def refresh_moon():
    astro.moon_data = {}
    astro.obs.date = now_time()
    astro.moon_info()

    moon_sign = rising_or_setting(next_transit_time=astro.moon_data['next_moon_transit'])
    moonaltstr = str(astro.moon_data['moon_alt'])
    moontext = "Moon " + moonaltstr +"° " + moon_sign
    Label(moon_frame, text=moontext, font='Arial 12 bold').grid(row=0, columnspan=2, padx=5, pady=5)

    moon_phase =  str(astro.moon_data['moon_phase_percent']) + "% " + astro.moon_data['moon_quarter'] + " " + astro.moon_data['moon_phase_name'] + " " + astro.moon_data['moon_phase_emoji']
    Label(moon_frame, text=moon_phase).grid(row=1, columnspan=2, padx=2, pady=2)
    next_moonrise_localtime = time_to_human(to_local(astro.moon_data['next_moonrise'].datetime()))
    Label(moon_frame, text="Next Moonrise:", justify="left").grid(row=2, column=0, padx=2, pady=2)
    Label(moon_frame, text=next_moonrise_localtime, justify="left").grid(row=2, column=1, padx=2, pady=2)
    next_moonset_localtime = time_to_human(to_local(astro.moon_data['next_moonset'].datetime()))
    Label(moon_frame, text="Next Moonset:", justify="left").grid(row=3, column=0, padx=2, pady=2)
    Label(moon_frame, text=next_moonset_localtime, justify="left").grid(row=3, column=1, padx=2, pady=2)
    next_fullmoon_localtime = time_to_human(to_local(astro.moon_data['next_full_moon'].datetime()))
    Label(moon_frame, text="Next Full Moon:", justify="left").grid(row=4, column=0, padx=2, pady=2)
    Label(moon_frame, text=next_fullmoon_localtime, justify="left").grid(row=4, column=1, padx=2, pady=2)
    next_newmoon_localtime = time_to_human(to_local(astro.moon_data['next_new_moon'].datetime()))
    Label(moon_frame, text="Next New Moon:", justify="left").grid(row=5, column=0, padx=2, pady=2)
    Label(moon_frame, text=next_newmoon_localtime, justify="left").grid(row=5, column=1, padx=2, pady=2)

def get_moon_data():
    day = 0
    moonrow = 2

    #Get local time offset
    timeoffset = datetime.now() - datetime.utcnow()
    timeoffsetsec = int(round(timeoffset.total_seconds() / 3600))

    #Set time to today at midnight
    today_midnight = datetime.now().replace(hour=0, minute=0)

    #convert today at midnight to UTC
    utc_datetime = today_midnight - timeoffset

    #Set up dictionaries to store data
    luna = {}

    while day < numdays:
       moondate = utc_datetime + timedelta(days=day)
       astro.moon_data =  {}

       display_date = moondate.strftime("%m/%d/%Y")


       astro.obs.date = moondate
       astro.obs.horizon = "-0:34"
       astro.obs.pressure = 0
       astro.moon_info()


       local_human_next_moonrise = time_to_human(to_local(astro.moon_data['next_moonrise'].datetime())).split()

       #Figure out if Moon rise is on different day (no rise on current day)
       d_day = display_date.split("/")
       md_day = local_human_next_moonrise[0].split("/")

       if int(d_day[1]) != int(md_day[1]):
           get_next_moonset_date = moondate
           moonrise_display = "-"
       else:
           get_next_moonset_date = astro.moon_data['next_moonrise'].datetime()
           moonrise_display = local_human_next_moonrise[1] + " " + local_human_next_moonrise[2] + " " + local_human_next_moonrise[3]

       astro.obs.date = get_next_moonset_date
       astro.moon_info()

       local_human_next_moonset = time_to_human(to_local(astro.moon_data['next_moonset'].datetime()))
       moonset_split = time_to_human(to_local(astro.moon_data['next_moonset'].datetime())).split()

       # Only dipslay set date if day is different
       if local_human_next_moonrise[0] == moonset_split[0]:
           moonset_display = moonset_split[1] + " " + moonset_split[2] + " " + moonset_split[3] 
       else: 
           moonset_display = local_human_next_moonset


       luna[display_date] = { 
               "Moonrise": moonrise_display,
               "Moonset": moonset_display,
               "Phase": astro.moon_data['moon_quarter'],
               "PhaseName": astro.moon_data['moon_phase_name'],
               "PhasePercent": astro.moon_data['moon_phase_percent'],
               "PhaseIcon": astro.moon_data['moon_phase_emoji'],
       }

       Label(moondata_frame, text=display_date).grid(row=moonrow, column=0, padx=2, pady=2)
       Label(moondata_frame, text=moonrise_display).grid(row=moonrow, column=1, padx=2, pady=2)
       Label(moondata_frame, text=moonset_display).grid(row=moonrow, column=2, padx=2, pady=2)
       moonphasedisplay = str(astro.moon_data['moon_phase_percent']) + "% " + astro.moon_data['moon_quarter'] + " " + astro.moon_data['moon_phase_name'] + " " + astro.moon_data['moon_phase_emoji'] 
       Label(moondata_frame, text=moonphasedisplay).grid(row=moonrow, column=3, padx=2, pady=2)
       day = day+1
       moonrow = moonrow+1


def refresh_button():
    refresh_moon()
    get_moon_data()


refresh_moon()
get_moon_data()


Button(bottom, text="Close", command=handle_button_press).grid(row=0, column=0)
Button(bottom, text="Refresh", command=refresh_button).grid(row=0, column=1)


root.mainloop()
