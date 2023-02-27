#! /usr/bin/env python3

import os
import tempfile
from xml.sax import saxutils

print('<?xml version="1.0" encoding="UTF-8"?>')
print('<osmChange version="0.6" generator="tiger_versus_python">')
print('<create>')

waysfile = tempfile.mkstemp()

waysfile_w = os.fdopen(waysfile[0],'w')


CARDINAL_DICT = {
    "N": "North",
    "E": "East",
    "S": "South",
    "W": "West"
}


def replace_cardinals(word):
    return CARDINAL_DICT.get(word, word)


ABBREV_DICT = {
    "Dr": "Drive",
    "St": "Street",
    "Sq": "Square",
    "Rd": "Road",
    "Blvd": "Boulevard",
    "Pkwy": "Parkway",
    "Cir": "Circle",
    "Ave": "Avenue",
    "Ct": "Court",
    "Ln": "Lane",
}


def replace_abbrev_words(word):
    return ABBREV_DICT.get(word, word)


def expand_abbreviations(street):
    parts = street.split(' ')
    if parts[0]=="St":
        parts[0]="Saint"
    if len(parts) > 2:
        for i in range(len(parts)):
            parts[i] = replace_cardinals(parts[i])
    for i in range(len(parts)):
        parts[i] = replace_abbrev_words(parts[i])
    street = " ".join(parts)

    # Clean up the data. There might be others as well.
    # e.g.: Milner''s Cres, Shelby, AL
    return street.replace("''", "'")


def print_full_address_node(next_id, node, house_number, street_name, county, state):
    print(f'<node id="{repr(next_id)}" lon="{node[0]}" lat="{node[1]}" visible="true" timestamp="1970-01-01T00:00:00Z" version="1">')
    print(f'<tag k="addr:housenumber" v="{house_number}" />')
    print(f'<tag k="addr:street" v={saxutils.quoteattr(street_name)} />')  # quoteattr adds the correct quotes.
    print(f'<tag k="addr:county" v={saxutils.quoteattr(county)} />')
    print(f'<tag k="addr:postcode" v="{postcode}" />')
    print(f'<tag k="addr:state" v="{state}" />')
    print("</node>")


FROM_COL = 0
TO_COL = 1
INTERPOLATION_COL = 2
STREET_COL = 3
CITY_COL = 4
STATE_COL = 5
POSTCODE_COL = 6
GEOMETRY_COL = 7

try:
    next_id = -2000000000

    while True:
        line = input()

        line_parts = line.split(';')

        # Skip header
        if line_parts[FROM_COL] == "from" and line_parts[TO_COL] == "to":
            continue

        geometry = line_parts[GEOMETRY_COL].split("(")[1].split(",")
        node_list = []

        first_node = geometry[0].split(' ')

        i=1
        while ')' not in geometry[i]:
            node_list.append(geometry[i].split(' '))
            i+=1

        last_node = geometry[i].split(')')[0].split(' ')

        first_house_number = line_parts[FROM_COL]
        last_house_number = line_parts[TO_COL]
        interpolation = line_parts[INTERPOLATION_COL]
        street_name = expand_abbreviations(line_parts[STREET_COL])
        county = line_parts[CITY_COL]
        state = line_parts[STATE_COL]
        postcode = line_parts[POSTCODE_COL]

        print_full_address_node(next_id, first_node, first_house_number, street_name, county, state)
        next_id+=1

        for node in node_list:
            print(f'<node id="{repr(next_id)}" lon="{node[0]}" lat="{node[1]}" visible="true" timestamp="1970-01-01T00:00:00Z" version="1" />')
            next_id+=1

        print_full_address_node(next_id, last_node, last_house_number, street_name, county, state)
        next_id+=1

        waysfile_w.write(f"{repr(next_id-len(node_list)-2)}\t{repr(next_id)}\t{interpolation}\n")

except EOFError:
    pass

del waysfile_w
waysfile_r = open(waysfile[1],'r')
os.unlink(waysfile[1])

for line in waysfile_r:
    line_parts = line.rstrip("\n").split('\t')
    print(f'<way id="{repr(next_id)}" visible="true" timestamp="1970-01-01T00:00:00Z" version="1">')
    for i in range(int(line_parts[0]),int(line_parts[1])):
        print(f'<nd ref="{repr(i)}" />')
    print(f'<tag k="addr:interpolation" v="{line_parts[2]}" />')
    print('<tag k="addr:inclusion" v="potential" />')
    print("</way>")
    next_id+=1

print("</create>")
print("</osmChange>")
