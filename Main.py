'''

    Travis Seal
    Main.py
    Driver file for auditing the OpenStreetMap data

'''
import codecs
import pprint
import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow
from collections import Counter, defaultdict
from pymongo import MongoClient
import AuditStreet
import AuditState
import AuditZip

client = MongoClient()
db = client.datascience
posts = db.posts


INPUT_OSM_FILE = "C:\\Users\Travis\Desktop\DSWrangling\data\sample_output_south_carolina.osm"


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

        #begin way_tags shapping
        tags.clear()
        for elem in element.iter("tag"):
            dict = {'id' : element.attrib['id'],'key' : str(elem.attrib['k']),'value' : elem.attrib['v'],'type' : elem.attrib['k']}

            tags.append(dict)

    return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Main Function                        #
# ================================================== #

def process_map(file_in, validate):
    file_out = "{0}.json".format(file_in)
    with codecs.open(file_out, "w") as fo:
      for element in get_element(file_in, tags=('node', 'way')):


        #clean street data
        elem = AuditStreet.updateStreetElement(element)

        #clean zip data
        elem = AuditZip.updateZipElement(elem)
        #start spapping

        #clean state
        elem = AuditState.updateStateElement(elem)

        #shape it
        el = shape_element(elem)
        if el:
            #import the data into mongodb
            #post_id = posts.insert_one(el).inserted_id
            #print(post_id)
            pprint.pprint(el)


#start
data = process_map(INPUT_OSM_FILE, True)