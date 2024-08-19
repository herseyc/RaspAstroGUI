from tkinter import *
from get_gps import *
from raspastroinfo import AstroData
import time
import math
from rasp_calc_func import *
from datetime import datetime, timedelta, timezone

root = Tk()
root.title("Solar System")
root.maxsize(800, 600)
root.config(bg="skyblue")

def handle_button_press():
    root.destroy()

def now_time():
    utc_now = datetime.utcnow()
    return utc_now

# GPS Frame
left_frame = Frame(root, width=400)
left_frame.grid(row=0, column=0, padx=10, pady=5)
Label(left_frame, text="GPS", font='Arial 12 bold').grid(row=0, columnspan=2, padx=5, pady=5)

# Visible Planets Frame
left_lowframe = Frame(root, width=400)
left_lowframe.grid(row=1, column=0, padx=10, pady=5)
Label(left_lowframe, text="Visible Planets", font='Arial 12 bold').grid(row=0, columnspan=2, padx=5, pady=5)

# Sun Frame
right_frame = Frame(root, width=400)
right_frame.grid(row=0, column=1, padx=10, pady=5)

# Moon Frame
right_lowframe = Frame(root, width=400)
right_lowframe.grid(row=1, column=1, padx=10, pady=5)

# Button Frame
bottom = Frame(root)
bottom.grid(rowspan=2, columnspan=2, padx=10, pady=5)


gps_data_tuple = get_gps_data()
gps_data = gps_data_tuple[6]

astro = {}
astro = AstroData(obslat=gps_data[1], obslon=gps_data[2], obslev=gps_data[3], obshorizon="-0:34", obsepoch=now_time())
astro.obs.pressure = 0


def refresh_gps():
   gps_data_tuple = get_gps_data()

   Label(left_frame, text="Fix:").grid(row=1, column=0, padx=2, pady=2)
   Label(left_frame, text=gps_data_tuple[0]).grid(row=1, column=1, padx=2, pady=2)
   Label(left_frame, text="Latitude:").grid(row=2, column=0, padx=2, pady=2)
   Label(left_frame, text=gps_data_tuple[1]).grid(row=2, column=1, padx=2, pady=2)
   Label(left_frame, text="Longitude:").grid(row=3, column=0, padx=2, pady=2)
   Label(left_frame, text=gps_data_tuple[2]).grid(row=3, column=1, padx=2, pady=2)
   Label(left_frame, text="Elevation:").grid(row=4, column=0, padx=2, pady=2)
   Label(left_frame, text=gps_data_tuple[3]).grid(row=4, column=1, padx=2, pady=2)



def refresh_sun():
    astro.sun_data = {}
    astro.obs.date = now_time()
    astro.sun_info()

    sun_sign = rising_or_setting(next_transit_time=astro.sun_data['next_sun_transit'])
    suntext = "Sun " + str(astro.sun_data['sun_alt']) +"° " + sun_sign

    Label(right_frame, text=suntext, font='Arial 12 bold').grid(row=0, columnspan=2, padx=5, pady=5)

    next_sunrise_localtime = time_to_human(to_local(astro.sun_data['next_sunrise'].datetime()))
    Label(right_frame, text="Next Sunrise:", justify="left").grid(row=1, column=0, padx=2, pady=2)
    Label(right_frame, text=next_sunrise_localtime, justify="left").grid(row=1, column=1, padx=2, pady=2)

    next_sunset_localtime = time_to_human(to_local(astro.sun_data['next_sunset'].datetime()))
    Label(right_frame, text="Next Sunset:", justify="left").grid(row=2, column=0, padx=2, pady=2)
    Label(right_frame, text=next_sunset_localtime, justify="left").grid(row=2, column=1, padx=2, pady=2)

    next_solstice_localtime = time_to_human(to_local(astro.sun_data['next_solstice'].datetime()))
    Label(right_frame, text="Next Solstice:", justify="left").grid(row=3, column=0, padx=2, pady=2)
    Label(right_frame, text=next_solstice_localtime, justify="left").grid(row=3, column=1, padx=2, pady=2)

    next_equinox_localtime = time_to_human(to_local(astro.sun_data['next_equinox'].datetime()))
    Label(right_frame, text="Next Equinox:", justify="left").grid(row=4, column=0, padx=2, pady=2)
    Label(right_frame, text=next_equinox_localtime, justify="left").grid(row=4, column=1, padx=2, pady=2)


def refresh_moon():
    astro.moon_data = {}
    astro.obs.date = now_time()
    astro.moon_info()

    moon_sign = rising_or_setting(next_transit_time=astro.moon_data['next_moon_transit'])
    moonaltstr = str(astro.moon_data['moon_alt'])
    moontext = "Moon " + moonaltstr +"° " + moon_sign
    Label(right_lowframe, text=moontext, font='Arial 12 bold').grid(row=0, columnspan=2, padx=5, pady=5)

    moon_phase =  str(astro.moon_data['moon_phase_percent']) + "% " + astro.moon_data['moon_quarter'] + " " + astro.moon_data['moon_phase_name'] + " " + astro.moon_data['moon_phase_emoji']
    Label(right_lowframe, text=moon_phase).grid(row=1, columnspan=2, padx=2, pady=2)
    next_moonrise_localtime = time_to_human(to_local(astro.moon_data['next_moonrise'].datetime()))
    Label(right_lowframe, text="Next Moonrise:", justify="left").grid(row=2, column=0, padx=2, pady=2)
    Label(right_lowframe, text=next_moonrise_localtime, justify="left").grid(row=2, column=1, padx=2, pady=2)
    next_moonset_localtime = time_to_human(to_local(astro.moon_data['next_moonset'].datetime()))
    Label(right_lowframe, text="Next Moonset:", justify="left").grid(row=3, column=0, padx=2, pady=2)
    Label(right_lowframe, text=next_moonset_localtime, justify="left").grid(row=3, column=1, padx=2, pady=2)
    next_fullmoon_localtime = time_to_human(to_local(astro.moon_data['next_full_moon'].datetime()))
    Label(right_lowframe, text="Next Full Moon:", justify="left").grid(row=4, column=0, padx=2, pady=2)
    Label(right_lowframe, text=next_fullmoon_localtime, justify="left").grid(row=4, column=1, padx=2, pady=2)
    next_newmoon_localtime = time_to_human(to_local(astro.moon_data['next_new_moon'].datetime()))
    Label(right_lowframe, text="Next New Moon:", justify="left").grid(row=5, column=0, padx=2, pady=2)
    Label(right_lowframe, text=next_newmoon_localtime, justify="left").grid(row=5, column=1, padx=2, pady=2)


def refresh_planets():
   astro.obs.date = now_time()
   astro.planet_info()
   rowcount = 1

   if astro.mercury['alt'] > 0:
       mercury_sign = rising_or_setting(next_transit_time=astro.mercury['next_transit'])
       mercury = "Mercury " + str(astro.mercury['alt']) +"° " + mercury_sign
       Label(left_lowframe, text=mercury).grid(row=rowcount, columnspan=2, padx=2, pady=2)
       rowcount += 1

   if astro.venus['alt'] > 0:
       venus_sign = rising_or_setting(next_transit_time=astro.venus['next_transit'])
       venus = "Venus " + str(astro.venus['alt']) +"° " + venus_sign
       Label(left_lowframe, text=venus).grid(row=rowcount, columnspan=2, padx=2, pady=2)
       rowcount += 1

   if astro.mars['alt'] > 0:
       mars_sign = rising_or_setting(next_transit_time=astro.mars['next_transit'])
       mars = "Mars " + str(astro.mars['alt']) +"° " + mars_sign
       Label(left_lowframe, text=mars).grid(row=rowcount, columnspan=2, padx=2, pady=2)
       rowcount += 1

   if astro.jupiter['alt'] > 0:
       jupiter_sign = rising_or_setting(next_transit_time=astro.jupiter['next_transit'])
       jupiter = "Jupiter " + str(astro.jupiter['alt']) +"° " + jupiter_sign
       Label(left_lowframe, text=jupiter).grid(row=rowcount, columnspan=2, padx=2, pady=2)
       rowcount += 1

   if astro.saturn['alt'] > 0:
       saturn_sign = rising_or_setting(next_transit_time=astro.saturn['next_transit'])
       saturn = "Saturn " + str(astro.saturn['alt']) +"° " + saturn_sign
       Label(left_lowframe, text=saturn).grid(row=rowcount, columnspan=2, padx=2, pady=2)
       rowcount += 1

   if astro.uranus['alt'] > 0:
       uranus_sign = rising_or_setting(next_transit_time=astro.uranus['next_transit'])
       uranus = "Uranus " + str(astro.uranus['alt']) +"° " + uranus_sign
       Label(left_lowframe, text=uranus).grid(row=rowcount, columnspan=2, padx=2, pady=2)
       rowcount += 1

   if astro.neptune['alt'] > 0:
       neptune_sign = rising_or_setting(next_transit_time=astro.neptune['next_transit'])
       neptune = "Neptune " + str(astro.neptune['alt']) +"° " + neptune_sign
       Label(left_lowframe, text=neptune).grid(row=rowcount, columnspan=2, padx=2, pady=2)
       rowcount += 1

   if astro.pluto['alt'] > 0:
       pluto_sign = rising_or_setting(next_transit_time=astro.pluto['next_transit'])
       pluto = "Pluto " + str(astro.pluto['alt']) +"° " + pluto_sign
       Label(left_lowframe, text=pluto).grid(row=rowcount, columnspan=2, padx=2, pady=2)
       rowcount += 1

def refresh_button():
    refresh_sun()
    refresh_moon()
    refresh_gps()
    refresh_planets()

refresh_gps()

refresh_planets()

refresh_sun()

refresh_moon()

Button(bottom, text="Close", command=handle_button_press).grid(row=0, column=0)
Button(bottom, text="Refresh", command=refresh_button).grid(row=0, column=1)


root.mainloop()
