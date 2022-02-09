#!/usr/bin/env python

"""Run this script on the command line via:

  python2 03-create_header.py > sm_map.cpp

It reads in a map, and outputs a hard-coded version of it in C++.

This script is not ready yet.

"""

import sys

import cPickle as pickle
from simple_graph import *

if __name__ == '__main__':

    with open("pickle/sgraph.p","rb") as f:     sgraph = pickle.load(f)
    i_fmt = '  nodes[%d] = map->add_intersection(%d,%.8f,%.8f);'
    s_fmt = '  map->add_street(%d,nodes[%d],nodes[%d],"%s",%d);'

    print '#include "map.h"'
    print ''
    print 'Map::Intersection** make_marietta_nodes(Map::Map* map) {'
    print '  Map::Intersection** nodes = (Map::Intersection**)malloc(sizeof(Map::Intersection*)*13045);'

    for node_id in sgraph.nodes:
        lat,lon = sgraph.nodes[node_id]
        print i_fmt % (node_id,node_id,lat,lon)
        """
        counter += 1
        if counter % 10 == 0:
            print ''
        """
    print '  return nodes;'
    print '}'

    print 'void make_marietta_edges(Map::Map* map, Map::Intersection** nodes) {'
    for edge_id in sgraph.edges:
        x_id,y_id,name,length = sgraph.edges[edge_id]
        print s_fmt % (edge_id,x_id,y_id,name,int(length))
        """
        counter += 1
        if counter % 10 == 0:
            print ''
        """
    print '}'

    print 'Map::Map* make_marietta_map() {'
    print '  Map::Map* map = new Map::Map;'
    print '  Map::Intersection** nodes = make_marietta_nodes(map);'
    print '  make_marietta_edges(map,nodes);'
    print '  free(nodes);'
    print '  return map;'
    print '}'

