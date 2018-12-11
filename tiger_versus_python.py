#! /usr/bin/env python

print "<?xml version='1.0' encoding='UTF-8'?>"
print '<osmChange version="0.6" generator="tiger_versus_python">'
print '<create>'

ways = []

def replace_cardinals(word):
    if word=='N':
        return "North"
    elif word=='E':
        return "East"
    elif word=='S':
        return "South"
    elif word=='W':
        return "West"
    return word

def replace_abbrev_words(word):
    if word=="Dr":
        return "Drive"
    elif word=="St":
        return "Street"
    elif word=="Sq":
        return "Square"
    elif word=="Rd":
        return "Road"
    elif word=="Blvd":
        return "Boulevard"
    elif word=="Pkwy":
        return "Parkway"
    elif word=="Cir":
        return "Circle"
    elif word=="Ave":
        return "Avenue"
    elif word=="Ct":
        return "Court"
    elif word=="Ln":
        return "Lane"
    return word

def expand_abbreviations(street):
    parts = street.split(' ')
    if parts[0]=="St":
        parts[0]="Saint"
    if len(parts) > 2:
        for i in range(len(parts)):
            parts[i] = replace_cardinals(parts[i])
    for i in range(len(parts)):
        parts[i] = replace_abbrev_words(parts[i])
    return " ".join(parts)

try:
    next_id = -2000000000
    while True:
        line = raw_input()
        line_parts = line.split(',')

        node_list = []
        first_node = line_parts[0].split('(')
        first_node = first_node[len(first_node)-1].split(' ')

        i=1
        while ')' not in line_parts[i]:
            node_list.append(line_parts[i].split(' '))
            i+=1
        
        last_node = line_parts[i].split(')')[0].split(' ')

        i+=2
        first_house_number = line_parts[i]
        i+=1
        last_house_number = line_parts[i]
        i+=1
        interpolation = line_parts[i]
        i+=1
        street_name = line_parts[i]
        while street_name[len(street_name)-1]!="'":
            i+=1
            street_name+=','+line_parts[i]
        street_name = street_name.replace('"',"&quot;").replace("'",'"').replace('""',"'").replace('&',"&amp;").replace('<',"&lt;").replace('>',"&gt;").strip(' "')
        street_name = '"'+expand_abbreviations(street_name)+'"'
        i+=1
        county = line_parts[i]+"'"
        i+=1
        state = "'"+line_parts[i][1:]
        i+=1
        postcode = line_parts[i].split(')')[0]

        print "<node id='"+repr(next_id)+"' lon='"+first_node[0]+"' lat='"+first_node[1]+"' visible='true' timestamp='1970-01-01T00:00:00Z' version='1'>"
        print "<tag k='addr:housenumber' v="+first_house_number+" />"
        print "<tag k='addr:street' v="+street_name+" />"
        print "<tag k='addr:county' v="+county+" />"
        print "<tag k='addr:postcode' v="+postcode+" />"
        print "<tag k='addr:state' v="+state+" />"
        print "</node>"
        next_id+=1

        for node in node_list:
            print "<node id='"+repr(next_id)+"' lon='"+node[0]+"' lat='"+node[1]+"' visible='true' timestamp='1970-01-01T00:00:00Z' version='1' />"
            next_id+=1

        print "<node id='"+repr(next_id)+"' lon='"+last_node[0]+"' lat='"+last_node[1]+"' visible='true' timestamp='1970-01-01T00:00:00Z' version='1'>"
        print "<tag k='addr:housenumber' v="+last_house_number+" />"
        print "<tag k='addr:street' v="+street_name+" />"
        print "<tag k='addr:county' v="+county+" />"
        print "<tag k='addr:postcode' v="+postcode+" />"
        print "<tag k='addr:state' v="+state+" />"
        print "</node>"
        next_id+=1

        ways.append((range(next_id-len(node_list)-2,next_id),interpolation))

except EOFError:
    pass

for way in ways:
    print "<way id='"+repr(next_id)+"' visible='true' timestamp='1970-01-01T00:00:00Z' version='1'>"
    for i in way[0]:
        print "<nd ref='"+repr(i)+"' />"
    print "<tag k='addr:interpolation' v="+way[1]+" />"
    print "<tag k='addr:inclusion' v='potential' />"
    print "</way>"
    next_id+=1

print "</create>"
print "</osmChange>"
