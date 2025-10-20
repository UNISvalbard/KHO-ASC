# -*- coding: utf-8 -*-
"""
Created on 2025/10/20

@author: Mikko Syrjäsuo/University Centre in Svalbard

The All-Sky video Camera (ASC) uses an image intensifier. To protect the
intensifier there is a mechanical shutter as well as extra control
electronics with a light sensor to prevent accidental use of the camera
when the ambient light levels are too high.

This short program computers the altitude of the Sun and the Moon and,
based on the results, opens the shutter and powers the intensifier
whenever:
   - the Sun is more than 12 degrees below the horizon
   - the Moon's altitude is less than +1 degrees above the horizon

"""

SUN_ANGLE_MAX_DEGREES = -12
MOON_ANGLE_MAX_DEGREES = 1


import numpy as np
import time
import astropy.units as u
from astropy.constants import R_earth
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz
from astropy.coordinates import get_sun, get_body
from astroplan.moon import moon_illumination, moon_phase_angle


def main():
    print("KHO ASC control program")
    print(f"- maximum solar altitude {SUN_ANGLE_MAX_DEGREES} degrees")
    print(f"- maximum lunar altitude {MOON_ANGLE_MAX_DEGREES} degrees")
    print()
    print("Press Ctrl-C to exit")

    showUpdate = True  # A flag to show the altitudes just once within the second

    try:
        while True:
            start = time.time()
            mytime = Time.now()
            kho = EarthLocation(lat=78.148*u.deg, lon=16.043*u.deg, height=520*u.m)
            obs_frame = AltAz(obstime=mytime, location=kho)
            sunaltaz = get_sun(mytime).transform_to(obs_frame)
            moonaltaz = get_body("moon",mytime,location=kho).transform_to(obs_frame)
            end = time.time()
            if sunaltaz.alt.deg < SUN_ANGLE_MAX_DEGREES:
                if moonaltaz.alt.deg < MOON_ANGLE_MAX_DEGREES:
                    print("    - Open shutter")

            if  mytime.value.second%10 == 0:
                if showUpdate==True:
                    showUpdate = False
                    print(f"Execution time: {end - start:.6f} seconds")
                    print("KHO observations at",mytime)
                    print("- solar altitude %.1f degrees" % sunaltaz.alt.deg)
                    print("- Moon altitude %.1f degrees" % moonaltaz.alt.deg)
                    #moonillum = np.max(moon_illumination(mytime))*100
                    #print("- Moon illumination %.1f %%" % moonillum)
            else:
                showUpdate = True
            time.sleep(0.1) # Add a small delay to reduce the CPU load
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()

