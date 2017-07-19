'''
    Travis Seal
    Find distinct addr:state tags
    Define mapping
'''
import pprint
import re
from collections import defaultdict

state_type_re = re.compile('sc', re.IGNORECASE)
state_types = defaultdict(set)
stateNamesNotFound = []
state_types = defaultdict(set)

expected = ['SC','sc']

state_mapping = \
{
    "sc":"SC",
    "South Carolina" : "SC"
}

#determines if the element is a state name
def is_state_name(tag):
    if tag.attrib["k"] == "addr:state":
        return True
    else:
        return False

'''
    check if there is a mapping for this state type, if there is, update the name.
    input: tag element
    return: updated elem object
'''
def updateStateElement(elem):
    st_types = audit_states(elem)
    for tag in elem.iter("tag"):
        if is_state_name(tag):
            betterName = update_name(tag.attrib['v'],state_mapping)
            print('Before updated: ',tag.attrib['v'])
            print('After updated: ', betterName)
            tag.attrib['v'] = betterName
            return elem
    return elem

def getLengthOfRoadEndingName(name):
    m = state_type_re.search(name)
    name = m.group()
    for k,v in state_mapping.items():
        if name == k:
            return len(k)
    return 0

'''
    adds names to list that are not found
    inputs: name of the street, mapping
'''
def update_name(name, mapping):
    print('input name is : ' , name)
    m = state_type_re.search(name)
    print('name var = : ', name)
    count = 0
    for k,v in mapping.items():
        count = count + 1
        if name == k or name in expected:
            return v
        elif name != k and count == len(mapping)-1 and name not in mapping:
            print('name is != key: ', name , '' , k)
            stateNamesNotFound.append(name)
    return ''


def audit_states(elem):
    if elem.tag == "node" or elem.tag == 'way':
        for tag in elem.iter("tag"):
            if is_state_name(tag):
                audit_state_type(state_types, tag.attrib['v'])
    return state_types



''' 
    find unexpected street names
    input: value of attribute of the tag
           street_types 
    Does not return values. only keeps track of the unexpected names.
'''
def audit_state_type(state_types, state_name):
    m = state_type_re.search(state_name)
    if m: #if its a street that we are looking for (St. Ave. etc..)
        street_type = m.group()
        print(street_type)
        if street_type not in expected:
            print('we did not exptect to see: ', street_type)
            state_types[street_type].add(state_name)
            stateNamesNotFound.append(state_name)