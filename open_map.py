import esy.osm.pbf

import configparser, contextlib
import os, sys
from esy.osmfilter import osm_colors as CC
from esy.osmfilter import run_filter 
from esy.osmfilter import Node, Way, Relation
import geocoder


# g = geocoder.osm('Belo Horizonte, MG, Brazil')
# print('Lat: {}\nLong: {}'.format(g.osm['y'], g.osm['x']))
# osm = esy.osm.pbf.File('north-america-latest.osm.pbf')

# city = [entry for entry in osm if entry.tags.get('city') == 'Oakland']

PBF_inputfile = os.path.join(os.getcwd(),
                  'north-america-latest.osm.pbf')


JSON_outputfile = os.path.join(os.getcwd(),'output.json')

prefilter   = {Node: {}, Way: {"name":["Oakland",],}, Relation: {2833530}}
print("Done")
blackfilter=[("name","shit")]
whitefilter=[[("name","Oakland")]]

[Data,_]=run_filter('pipelines',PBF_inputfile, JSON_outputfile, prefilter,whitefilter, blackfilter, NewPreFilterData=True, CreateElements=True, LoadElements=False,verbose=True)