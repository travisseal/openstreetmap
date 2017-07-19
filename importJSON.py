'''
    imports json into mongo
    Some manual work: you must specify way/node when you import data
    At this time, no check on the type of object exists...
    
'''
from collections.abc import Mapping

from pymongo import MongoClient, collection
import ijson

client = MongoClient()
db = client.datascience
posts = db.posts


filename = "E:\Projects\Python\Intro DataScience\data\output.json"



with open(filename, 'r') as f:
    #change .way to .node each time data is imported.
    objects = ijson.items(f,'osm.node')

    '''
        Sometimes the data returned from iterating the xml comes back as an array with embedded dictionaries.
        Solution was to iterate the array, cast each element as a dictionary, then insert. All based on the 
        check using 'instance'
    '''

    for item in objects:
        #print(item)
        if isinstance(item, list):
          newid = 'node' #processing way objects
          newDict = {}
          newDict.__setitem__(str(newid),item)
         # post_id = posts.insert_one(newDict).inserted_id
          print(item)


        #elif isinstance(item,dict):
           #post_id = posts.insert_one(dict(item)).inserted_id

        elif isinstance(item,dict) == False and isinstance(item,list) == False:
            print('Data was something else other than a list or a dictionary... Failing to insert the following: ', item)


