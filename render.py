__author__ = 'zlanka'

import json
import math
import subprocess
from subprocess import PIPE

countries_blacklist = []
cities_blacklist = []

debug = False

threads = 8
min_zoom = 2
max_zoom = 15
styles = ['osm', 'style_retina']


def lat2num(lat_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    y = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return y


def lon2num(lon_deg, zoom):
    n = 2.0 ** zoom
    x = int((lon_deg + 180.0) / 360.0 * n)
    return x


def render_tiles(min_x, max_x, min_y, max_y, zoom):
    for style in styles:
        style_arg = '' if (style == 'osm') else " -m 'style_retina'"
        cmd = "render_list -a -n 8 -x " + str(min_x) + " -X " + str(max_x) + " -y " + str(min_y) + " -Y " + str(max_y) + " -z " + str(zoom) + " -Z " + str(zoom) + style_arg
        subprocess.call(cmd, shell=True, stdout=PIPE)
    pass


def add_city_tiles(city_details):
    if city_details['name'] in cities_blacklist or city_details['country_name'] in countries_blacklist:
        return
    for zoom in range(min_zoom, max_zoom):
        min_lat, max_lat = city_details['lat'] - 0.25, city_details['lat'] + 0.25
        min_lon, max_lon = city_details['lon'] - 0.25, city_details['lon'] + 0.25
        min_x = lon2num(min_lon, zoom)
        max_x = lon2num(max_lon, zoom)
        min_y = lat2num(min_lat, zoom)
        max_y = lat2num(max_lat, zoom)
        render_tiles(min_x, max_x, min_y, max_y, zoom)
    print('done for city ' + city_details['name'].encode('utf8'))


def main():
    with open('data/cities_lat_lons.json', 'r') as f:
        data = json.load(f)
        for city_details in data:
            add_city_tiles(city_details)


if __name__ == '__main__':
    main()
