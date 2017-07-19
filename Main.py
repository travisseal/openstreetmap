'''

    Travis Seal
    Main.py
    Driver file for auditing the OpenStreetMap data

'''
import codecs
import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow
from collections import Counter, defaultdict

import json

import AuditStreet
import AuditState
import AuditZip

INPUT_OSM_FILE = "C:\\Users\Travis\Desktop\DSWrangling\data\sample_output_south_carolina.osm"
OUTPUT_JSON = "C:\\Users\Travis\Desktop\DSWrangling\data\output_south_carolina.json"

d = defaultdict(int)
dictUniqueStartTags = {}


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
    node = {}
    if element.tag == "node" or element.tag == "way":
        for tag in element.iter("tag"):
            node.__setitem__(tag.attrib['k'],tag.attrib['v'])
            print(node)
        return node
    else:
        return None

def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


data = process_map(INPUT_OSM_FILE, True)