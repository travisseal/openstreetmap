'''

    Travis Seal
    Main.py
    Driver file for auditing the OpenStreetMap data

'''
import codecs
import pprint
import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow
from collections import Counter, defaultdict
import cerberus
import json
import SCHEMA

import AuditStreet
import AuditState
import AuditZip
INPUT_OSM_FILE = "C:\\Users\Travis\Desktop\DSWrangling\data\sample_output_south_carolina.osm"
OUTPUT_JSON = "C:\\Users\Travis\Desktop\DSWrangling\data\output_south_carolina.json"

d = defaultdict(int)
dictUniqueStartTags = {}

node_attribs = {}
way_attribs = {}
way_nodes = []
tags = []  # Handle secondary tags the same way for both node and way elements

NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']



def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference: The below code was inspired by the below reference:
    
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)


    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def shape_element(element):

    if element.tag == 'node':
        for elem in element.attrib:
            for nField in NODE_FIELDS:
                if elem == nField:
                    node_attribs.__setitem__(nField,element.attrib[elem])


        return {'node': node_attribs, 'node_tags': tags}

    elif element.tag == 'way':
        for el in element.attrib:
           for wField in WAY_FIELDS:
              if el == wField:
                way_attribs.__setitem__(wField,element.attrib[el])

        wnCounter = 0
        way_nodes.clear()
        for tag in element.iter("nd"):
            attribDict = tag.attrib
            tempDict = {'id':element.attrib['id'], 'node_id': attribDict.get('ref'), 'Position' :wnCounter}
            way_nodes.append(tempDict)
            wnCounter = wnCounter + 1

    return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

#Schema validation
def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)

        raise Exception(message_string.format(field, error_string))


# ================================================== #
#               Main Function                        #
# ================================================== #

def process_map(file_in, validate):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                pprint.pprint(el)
               # if validate is True:
                #    validate_element(el, validator)



data = process_map(INPUT_OSM_FILE, True)