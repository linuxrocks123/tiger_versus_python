#! /usr/bin/env python3

import json
import string
import sys
import re

#This data is of absolutely awful quality, so longitude and latitude are sometimes reversed.
#Fix this appropriately if your data is not in the Northern Western quadrant of the Earth.
def fix_swapped_coordinates(coords):
    if coords[0] >= 0:
        coords[0], coords[1] = coords[1], coords[0]
        sys.stderr.write("Corrected fucked JSON coordinates to "+repr(coords)+'\n')
    return coords

#And also occasionally a street in Texas will be located at the South Pole.
def data_is_fucked(coords):
    MIN_LON = -180
    MAX_LON = 0
    MIN_LAT = 0
    MAX_LAT = 90
    return coords[0] <= MIN_LON or coords[0] >= MAX_LON or coords[1] <= MIN_LAT or coords[1] >= MAX_LAT

tokens = str.split(sys.argv[1],'/')
default_state = tokens[-2].upper()

default_city = ""
default_county = ""

file_tokens = tokens[-1].split('.')[0].split('-')
if file_tokens[-1]=="city":
    default_city = file_tokens[0].replace('_',' ').upper()
elif file_tokens[-1]=="county":
    default_county = file_tokens[0].replace('_',' ').upper()

# All control characters (ASCII 0 - 31 and 127).
CONTROL_CHARS_RE = re.compile(r'[\x00-\x1F\x7F]')

for line in map(str.rstrip,open(sys.argv[1]).readlines()):
    try:
        address_object = json.loads(line)
    except:
        sys.stderr.write("Invalid line: "+line+'\n')
        continue

    #Some basic sanity checks since the data isn't sane
    if 'properties' not in address_object or not address_object['properties'] or 'geometry' not in address_object or not address_object['geometry'] or 'coordinates' not in address_object['geometry'] or not address_object['geometry']['coordinates']:
        continue

    properties = address_object['properties']
    if 'number' not in properties or properties['number']=="" or 'street' not in properties or properties['street']=="":
        continue

    row = [""] * 8
    row[0] = properties['number']
    row[1] = row[0]
    row[2] = "NARF"
    row[3] = properties['street']
    row[4] = properties['city'] if properties['city']!="" else default_city
    row[5] = properties['region'] if properties['region']!="" else default_state
    row[6] = properties['postcode']
    coords = address_object['geometry']['coordinates']

    coords = fix_swapped_coordinates(coords)
    if data_is_fucked(coords):
        sys.stderr.write("Skipping fucked-beyond-repair JSON coordinates of "+repr(coords)+'\n')
        continue

    row[7] = '('+repr(coords[0])+' '+repr(coords[1])
    row = [string.capwords(x) for x in row]
    row[5] = row[5].upper()
    row = [x.replace(';', '#') for x in row]
    row = [CONTROL_CHARS_RE.sub('', x) for x in row]
    print(";".join(row))
