#!/usr/bin/env jython

# export CLASSPATH=lib:lib/graphhopper-web-0.8-SNAPSHOT-with-dep.jar:lib/graphhopper-map-matching-0.8-SNAPSHOT-jar-with-dependencies.jar

# https://www.openstreetmap.org/export#map=15/33.9470/-84.5259

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

def simulate_trace(s,t):
    """
    given starting GPS coordinates s and ending GPS coordinates t,
    simulate a GPS trace that can be passed into the map matcher

    """
    #s = (33.995509,-118.476703)
    #t = (34.016788,-118.472621)
    steps = 10
    total_time = 3600
    start_time = 1213084000
    trip = []

    for i in range(steps+1):
        lat,lon = s[0] + i*(t[0]-s[0])/steps,s[1] + i*(t[1]-s[1])/steps
        time = start_time + i*total_time/steps
        trip.append((lat,lon,time))
    return trip

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
        except java.lang.Exception, exception:
            print "skipping: %s" % exception
            continue
    return matches

def zero():
    return 0

if __name__ == '__main__':
    filename = "xml/map.osm"
    tmp_dir = "./tmp"
    s = (33.93766,-84.52020)  # Atrium building
    t = (33.95230,-84.54935)  # sweet treats

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
    #print sgraph


    # create MapMatching object, can and should be shared accross threads
    locationIndex = LocationIndexMatch(graph,hopper.getLocationIndex())
    mapMatching = MapMatching(graph,locationIndex,encoder)

    trip = simulate_trace(s,t)
    matches = trips_to_gh([trip],mapMatching)
    print "trips: %d/1 matched" % len(matches)
    match = matches[0]
    saved_match = []
    for point in match:
        edge = point.getEdgeState()
        x,y = edge.getBaseNode(),edge.getAdjNode()
        if y < x: x,y = y,x
        pair = (x,y)
        saved_match.append(pair)

    s = set(saved_match[0]) - set(saved_match[1])
    t = set(saved_match[-1]) - set(saved_match[-2])
    print "start node is %d" % s.pop()
    print "  end node is %d" % t.pop()
