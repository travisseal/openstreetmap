'''
    converts cleaned up osm file into json
'''

import pprint
import xmltodict as x
import json

'''
https://pythonadventures.wordpress.com/2014/12/29/xml-to-dict-xml-to-json/
'''




def convert(xml_file, xml_attribs=True):
    with open(xml_file, "rb") as f:
        d = x.parse(f, xml_attribs=xml_attribs)
        #pprint.pprint(d)
        file = open("E:\Projects\Python\Intro DataScience\data\output.json", "w")
        json.dump(d,file)
        file.close()


convert('E:\Projects\Python\Intro DataScience\data\output_south_carolina.osm')