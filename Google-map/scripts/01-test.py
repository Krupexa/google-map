#!/usr/bin/env jython

"""This script reads in an openstreetmap XML map, and converts it to
a simpler python data structure.  The included map was downloaded from
here:

  https://www.openstreetmap.org/export#map=15/33.9470/-84.5259

either click "export", and if that doesn't work click "Overpass API"

To run this script, you need jython, and you need the graphhopper
library.  I included the version I used, under lib.  You need to tell
jython where it is, with this command:

  export CLASSPATH=lib:lib/graphhopper-web-0.8-SNAPSHOT-with-dep.jar:lib/graphhopper-map-matching-0.8-SNAPSHOT-jar-with-dependencies.jar

To run the script, run "jython 01-test.py" on the command line.  It
assumes the map is under the xml/ directory.  It saves a python
version of the map under the pickle/ directory.

"""

import glob
import math
from collections import defaultdict
from operator import itemgetter

import com.graphhopper.GraphHopper as GraphHopper
import com.graphhopper.storage.GraphHopperStorage as GraphHopperStorage
import com.graphhopper.reader.osm.GraphHopperOSM as GraphHopperOSM
import com.graphhopper.routing.util.CarFlagEncoder as CarFlagEncoder
import com.graphhopper.routing.util.EncodingManager as EncodingManager

import com.graphhopper.matching.MapMatching as MapMatching
import com.graphhopper.matching.LocationIndexMatch as LocationIndexMatch
import com.graphhopper.util.GPXEntry as GPXEntry

import java.lang.Exception

from simple_graph import *

def simple_graph(graph):
    nodes,edges = {},{}
    node_iterator = graph.getNodeAccess()
    edge_iterator = graph.getAllEdges()
    while edge_iterator.next():
        edge_id = edge_iterator.getEdge()
        edge_name = edge_iterator.getName()
        edge_length = edge_iterator.getDistance()
        x,y = edge_iterator.getBaseNode(),edge_iterator.getAdjNode()

        if x not in nodes:
            lat,lon = node_iterator.getLat(x),node_iterator.getLon(x)
            nodes[x] = (lat,lon)
        if y not in nodes:
            lat,lon = node_iterator.getLat(y),node_iterator.getLon(y)
            nodes[y] = (lat,lon)

        if y < x: x,y = y,x
        edges[edge_id] = (x,y,edge_name,edge_length)

    return SimpleGraph(nodes,edges)

def read_trips(filename):
    trips,last_occ = [],0
    with open(filename,'r') as f:
        for line in f.readlines():
            line = line.strip().split(' ')
            occ = int(line[2])
            if occ == 0: pass
            if occ == 1:
                if last_occ == 0: trips.append([])
                lat,lon,time = float(line[0]),float(line[1]),long(line[3])
                trips[-1].append((lat,lon,time))
            last_occ = occ

    # sort by time
    for trip in trips:
        trip.sort(key=itemgetter(2))

    return trips

def trip_to_gh(trip):
    gtrip = []
    for lat,lon,time in trip:
        entry = GPXEntry(lat,lon,time)
        gtrip.append(entry)
    return gtrip

def trips_to_gh(trips,mapMatching):
    matches = []
    for trip in trips:
        if len(trip) <= 2 :
            #print "skipping: length %d" % len(trip)
            continue
        gtrip = trip_to_gh(trip)
        try:
            match = mapMatching.doWork(gtrip).getEdgeMatches()
            matches.append(match)
        except java.lang.Exception:
            #print "skipping: %s" % exception
            continue
    return matches

def zero():
    return 0

if __name__ == '__main__':
    filename = "xml/map.osm"
    tmp_dir = "./tmp"

    hopper = GraphHopperOSM()
    hopper.setStoreOnFlush(False)
    hopper.setOSMFile(filename)
    hopper.setGraphHopperLocation(tmp_dir)
    encoder = CarFlagEncoder()
    hopper.setEncodingManager(EncodingManager([encoder]))
    hopper.setCHEnabled(False)

    hopper.importOrLoad()
    graph = hopper.getGraphHopperStorage()
    base_graph = graph.getBaseGraph()

    sgraph = simple_graph(base_graph)

    # create MapMatching object, can and should be shared accross threads
    locationIndex = LocationIndexMatch(graph,hopper.getLocationIndex())
    mapMatching = MapMatching(graph,locationIndex,encoder)

    total_trips = 0
    total_match = 0

    """
    # this part takes GPS data and maps it to a path on the graph
    filenames = sorted(glob.glob("test/cabspottingdata/new_*.txt"))

    #used_nodes,used_edges = defaultdict(zero), defaultdict(zero)
    saved_matches = []
    for i,filename in enumerate(filenames):
        print "filename: %s (%d/%d)" % (filename,i+1,len(filenames))
        trips = read_trips(filename)
        matches = trips_to_gh(trips,mapMatching)
        print "trips: %d/%d matched" % (len(matches),len(trips))
        total_trips += len(trips)
        total_match += len(matches)

        for match in matches:
            saved_match = []
            for point in match:
                edge = point.getEdgeState()
                x,y = edge.getBaseNode(),edge.getAdjNode()
                if y < x: x,y = y,x
                pair = (x,y)
                #used_nodes[x] += 1
                #used_nodes[y] += 1
                #used_edges[pair] += 1
                saved_match.append(pair)
            saved_matches.append(saved_match)

    print "total trips: %d/%d matched" % (total_match,total_trips)
    #print "used nodes: %d/%d" % (len(used_nodes),len(sgraph.nodes))
    #print "used edges: %d/%d" % (len(used_edges),len(sgraph.edges))
    """

    import cPickle as pickle
    with open("pickle/sgraph.p","wb") as f: pickle.dump(sgraph,f)
    #with open("pickle/used_nodes.p","wb") as f: pickle.dump(used_nodes,f)
    #with open("pickle/used_edges.p","wb") as f: pickle.dump(used_edges,f)
    #with open("pickle/matches.p","wb") as f: pickle.dump(saved_matches,f)
