#! /usr/bin/env python3

import re
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
    "W": "West",
    "NE": "Northeast",
    "NW": "Northwest",
    "SE": "Southeast",
    "SW": "Southwest",
}


def replace_cardinals(word):
    return CARDINAL_DICT.get(word, word)


# Single word abbreviations from official TIGER docs:
# https://www2.census.gov/geo/pdfs/maps-data/data/tiger/tgrshp2023/TGRSHP2023_TechDoc_C.pdf
# https://www2.census.gov/geo/pdfs/maps-data/data/tiger/tgrshp2023/TGRSHP2023_TechDoc_D.pdf
ABBREV_DICT = {
    "Acc": "Access",
    "Acdmy": "Academy",
    "Alt": "Alternate",
    "Aly": "Alley",
    "Apts": "Apartments",
    "Arc": "Arcade",
    "Arprt": "Airport",
    "Ave": "Avenue",
    "Bch": "Beach",
    "Bk": "Bank",
    "Bldg": "Building",
    "Blf": "Bluff",
    "Blvd": "Boulevard",
    "Bnd": "Bend",
    "Br": "Branch",
    "Brg": "Bridge",
    "Brk": "Brook",
    "Bus": "Business",
    "Byp": "Bypass",
    "Byu": "Bayou",
    "Chnnl": "Channel",
    "Cir": "Circle",
    "Clb": "Club",
    "Clf": "Cliff",
    "Cmn": "Common",
    "Cmns": "Commons",
    "Cmpgrnd": "Campground",
    "Cmps": "Campus",
    "Cmtry": "Cemetery",
    "Cnl": "Canal",
    "Cnvnt": "Convent",
    "Colg": "College",
    "Complx": "Complex",
    "Con": "Connector",
    "Condo": "Condominium",
    "Condos": "Condominiums",
    "Cors": "Corners",
    "Cp": "Camp",
    "Cpl": "Chapel",
    "Cres": "Crescent",
    "Crk": "Creek",
    "Crs": "Course",
    "Crst": "Crest",
    "Cswy": "Causeway",
    "Ct": "Court",
    "Ctr": "Center",
    "Cts": "Courts",
    "Cv": "Cove",
    "Cyn": "Canyon",
    "Dep": "Depot",
    "Dept": "Department",
    "Dm": "Dam",
    "Dr": "Drive",
    "Drn": "Drain",
    "Dv": "Divide",
    "Ests": "Estates",
    "Exd": "Extended",
    "Exn": "Extension",
    "Expy": "Expressway",
    "Ext": "Extension",
    "Faclty": "Facility",
    "Fld": "Field",
    "Fls": "Falls",
    "Frk": "Fork",
    "Frm": "Farm",
    "Frst": "Forest",
    "Frtrnty": "Fraternity",
    "Ft": "Fort",
    "Fwy": "Freeway",
    "Gdns": "Gardens",
    "Gln": "Glen",
    "Grge": "Garage",
    "Grn": "Green",
    "Hbr": "Harbor",
    "Hl": "Hill",
    "Holw": "Hollow",
    "Hosp": "Hospital",
    "Hse": "House",
    "Hsng": "Housing",
    "Hst": "Historic",
    "Hts": "Heights",
    "Hwy": "Highway",
    "Inlt": "Inlet",
    "Inst": "Institute",
    "Instn": "Institution",
    "Is": "Island",
    "Iss": "Islands",
    "Lbry": "Library",
    "Ldg": "Lodge",
    "Lk": "Lake",
    "Lks": "Lakes",
    "Ln": "Lane",
    "Lndfll": "Landfill",
    "Lndg": "Landing",
    "Lp": "Loop",
    "Mdws": "Meadows",
    "Meml": "Memorial",
    "Mnmt": "Monument",
    "Mnr": "Manor",
    "Monstry": "Monastery",
    "Mrna": "Marina",
    "Mssn": "Mission",
    "Mt": "Mount",
    "Mtl": "Motel",
    "Mtn": "Mountain",
    "Mtwy": "Motorway",
    "Mus": "Museum",
    "Ofc": "Office",
    "Opas": "Overpass",
    "Orchrds": "Orchards",
    "Ovp": "Overpass",
    "Pkwy": "Parkway",
    "Pl": "Place",
    "Plnt": "Plant",
    "Plz": "Plaza",
    "Pr": "Prairie",
    "Prt": "Port",
    "Psge": "Passage",
    "Pt": "Point",
    "Pub": "Public",
    "Pvt": "Private",
    "Quar": "Quarry",
    "RR": "Railroad",
    "Rd": "Road",
    "Rdg": "Ridge",
    "Resrt": "Resort",
    "Resv": "Reserve",
    "Riv": "River",
    "Rlwy": "Railway",
    "Rmp": "Ramp",
    "Rte": "Route",
    "Schl": "School",
    "Scn": "Scenic",
    "Skwy": "Skyway",
    "Smry": "Seminary",
    "Snd": "Sound",
    "Spg": "Spring",
    "Spr": "Spur",
    "Sq": "Square",
    "St": "Street",
    "Sta": "Station",
    "Stra": "Stravenue",
    "Strm": "Stream",
    "Ter": "Terrace",
    "Tmpl": "Temple",
    "Tpke": "Turnpike",
    "Trak": "Track",
    "Trce": "Trace",
    "Trfy": "Trafficway",
    "Trl": "Trail",
    "Trmnl": "Terminal",
    "Tunl": "Tunnel",
    "Twr": "Tower",
    "Univ": "University",
    "Unp": "Underpass",
    "Upas": "Underpass",
    "Vlg": "Village",
    "Vly": "Valley",
    "Vw": "View",
    "Xing": "Crossing",
    "Xroad": "Crossroads",
}


def replace_abbrev_words(word):
    return ABBREV_DICT.get(word, word)


INTERSTATE_RE = re.compile(r"I- (?P<i_num>[0-9]+)")
NUMBER_STREET_RE = re.compile(r"(?P<s_num>[0-9]+) [tT][hH] ")
MC_STREET_RE = re.compile(r"Mc (?P<name>[a-zA-Z]+)")


def cleanup_full_street(street):
    # e.g.: "Milner''s Crescent" (Shelby, AL)
    street = street.replace("''", "'")

    # e.g.: "I- 19 Frontage Road", "I- 10"
    street = INTERSTATE_RE.sub(r"I-\g<i_num>", street)

    # e.g.: "5 Th Street Southwest"
    street = NUMBER_STREET_RE.sub(r"\g<s_num>th ", street)

    # e.g.: "Mc Clintock Avenue"
    street = MC_STREET_RE.sub(r"Mc\g<name>", street)

    return street


def expand_abbreviations(street):
    parts = street.split(' ')
    if parts[0]=="St":
        parts[0]="Saint"
    for i in range(len(parts)):
        parts[i] = replace_cardinals(parts[i])
    for i in range(len(parts)):
        parts[i] = replace_abbrev_words(parts[i])
    street = " ".join(parts)
    return cleanup_full_street(street)


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
