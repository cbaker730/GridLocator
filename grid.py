# pip3 install geopy
# pip install maidenhead

from argparse import ArgumentParser
from geopy.geocoders import Nominatim
import time
import sys
from pprint import pprint
import maidenhead as mh



def getGrid(city):

    # instantiate a new Nominatim client
    app = Nominatim(user_agent="tutorial")

    # get location raw data
    location = app.geocode(city).raw

    latitude = location["lat"]
    longitude = location["lon"]
    print(f"Coordinates and grid location for {city}:\n{latitude}, {longitude}")

    # Level Precision
    # 1     World           AA
    # 2     Regional        AA11
    # 3     Metropolis      AA11aa
    # 4     City            AA11aabb
    level = 3

    gridloc = mh.to_maiden(float(latitude), float(longitude), level)
    print(f"{gridloc}")


def getCoords(gridLoc):

    # instantiate a new Nominatim client
    app = Nominatim(user_agent="tutorial")

    # The --center option outputs lat lon of the center of provided maidenhead grid square
    # instead of the default southwest corner

    center = True

    #if args.mid:
    #    print(f"args.mid = true")
    #    center = bool(args.mid)

    coords = mh.to_location(gridLoc, center)
    if center:
        spot = "Center"
    else:
        spot = "Southwest corner"
    print(f"{spot} of grid {gridLoc}: \n{coords}")

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-c", "--city", help="Provide city name in format: --city \'Philadelphia, PA\'", type=str, action="store")
    parser.add_argument("-l", "--level", help="[TODO] Return the grid location precision [1-4] (default=3)", type=int, action="store")
    parser.add_argument("-g", "--grid", help="Provide grid location in format: --grid AA##aa", type=str, action="store")
    parser.add_argument("-m", "--mid", help="[TODO] Return coordinates of the center of the grid square, not the default southwest corner", type=bool, default=False)
    parser.add_argument("string", nargs="*")
    args = parser.parse_args()

    if args.city:
        cityName = args.city
        getGrid(cityName)
        sys.exit()

    if args.grid:
        gridLocation = args.grid
        getCoords(gridLocation)
        sys.exit()

    else:
        print("Insufficient arguments supplied. For help, use '-h' option. Exiting..")
        sys.exit()
