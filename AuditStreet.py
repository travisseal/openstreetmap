'''
    Travis Seal
    AuditStreet.py
    
    All the logic behind how to audit the street names of the file.
    07/11/2017
'''

import pprint
import re
from collections import defaultdict
import pandas as pd

#regex definitions
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_types = defaultdict(set)

streetNamesNotFound = []

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons","Gate",'Mall', 'Circle', 'Hwy' ,'Way']

street_mapping = \
        {   "St": "Street",
            "St.": "Street",
            "ST" : "Street",
            "Blvd" : "Boulevard",
            "Ct." : "Court",
            "D" : "Drive",
            "Dr" : "Drive",
            "Hwy" : "Highway",
            "Pkwy" : "Parkway",
            "RD" : "Road",
            "Rd" : "Road",
         }

#determines if the element is a street name
def is_street_name(tag):
    if tag.attrib["k"] == "addr:street":
        return True
    else:
        return False

'''
    check if there is a mapping for this street type, if there is, update the name.
    input: tag element
    return: updated elem object
'''
def updateStreetElement(elem):
    st_types = audit_streets(elem)
    for tag in elem.iter("tag"):
        if is_street_name(tag):
            betterName = update_name(tag.attrib['v'],street_mapping)
            length_to_trunc = getLengthOfRoadEndingName(tag.attrib['v'])
            updatedName = str(tag.attrib['v'])[:len(tag.attrib['v']) - int(length_to_trunc)] + str(betterName)
            tag.attrib['v'] = updatedName
            return elem
    return elem

def audit_streets(elem):
    if elem.tag == "node" or elem.tag == 'way':
        for tag in elem.iter("tag"):
            if is_street_name(tag):
                audit_street_type(street_types, tag.attrib['v'])
    #pprint.pprint(dict(street_types))
    return street_types

'''
    adds names to list that are not found
    inputs: name of the street, mapping
'''
def update_name(name, mapping):
    print('input name is : ' , name)
    m = street_type_re.search(name)
    name = m.group()
    print('name var = : ', name)
    count = 0
    for k,v in mapping.items():
        count = count + 1
        if name == k:
            return v
        elif name != k and count == len(mapping)-1 and name not in mapping:
            print('name is != key: ', name , '' , k)
            streetNamesNotFound.append(name)
    return ''

def getLengthOfRoadEndingName(name):
    m = street_type_re.search(name)
    name = m.group()
    for k,v in street_mapping.items():
        if name == k:
            return len(k)
    return 0



''' 
    find unexpected street names
    input: value of attribute of the tag
           street_types 
    Does not return values. only keeps track of the unexpected names.
'''
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m: #if its a street that we are looking for (St. Ave. etc..)
        street_type = m.group()
        #print('we found a match at ', street_type )
        if street_type not in expected:
            print('we did not exptect to see: ', street_type)
            street_types[street_type].add(street_name)
            streetNamesNotFound.append(street_name)



def printSummary():
    print("\n")
    print("Here is the unique list of unexpected road types: ", pd.unique(streetNamesNotFound))
    print("Street Types: " , pprint.pprint(street_types))
    print('values in mapping: ', pprint.pprint(street_mapping))