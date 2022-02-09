#!/usr/bin/env python

"""Run this script on the command line via:

  python2 02-example.py

It draws a map, and puts it under the maps/ directory.

Copy-and-paste the path printed out, into the variable path below.

The resulting map is saved as maps/path.png.

"""


import sys
import math
import random
import string

import gmplot
import staticmap
import cPickle as pickle
from collections import defaultdict
from simple_graph import *

class Stats:
    def __init__(self):
        self.min = sys.maxint
        self.max = 0
        self.sum = 0.0
        self.N = 0

    def __repr__(self):
        st = []
        st.append( "min: %d" % self.min )
        st.append( "max: %d" % self.max )
        avg = float(self.sum)/float(self.N)
        st.append( "avg: %.2f" % avg )
        st.append( "  N: %d" % self.N )
        return "\n".join(st)

    def update(self,x):
        self.min = min(self.min,x)
        self.max = max(self.max,x)
        self.sum += x
        self.N += 1

def zero():
    return 0

def path_endpoints(path):
    if len(path) == 1:
        s,t = path[0]
    else:
        x,y = path[0]
        s = x if y in path[1] else y
        x,y = path[-1]
        t = x if y in path[-2] else y
    return s,t

def nearest_nodes(lat,lon,graph):
    distances = []
    for node in graph.nodes:
        cur_lat,cur_lon = graph.nodes[node]
        dist = (lat-cur_lat)**2 + (lon-cur_lon)**2
        distances.append((node,dist))
    distances.sort(key=lambda x: x[1])
    return distances

# p is [0,1]
def get_color(p):
    from matplotlib.cm import hsv
    r,g,b,a = hsv(p)
    r,g,b = int(255*r),int(255*g),int(255*b)
    html = "#%02x%02x%02x" % (r,g,b)
    return html

def get_bounding_box(paths,sgraph):
    path = paths[0]
    node = path[0][0]
    min_lat = max_lat = sgraph.nodes[node][0]
    min_lon = max_lon = sgraph.nodes[node][1]
    for path in paths:
        for edge in path:
            for node in edge:
                lat,lon = sgraph.nodes[node]
                if lat < min_lat: min_lat = lat
                if lat > max_lat: max_lat = lat
                if lon < min_lon: min_lon = lon
                if lon > max_lon: max_lon = lon
    return [ (min_lat,min_lon), (max_lat,max_lon) ]

def lonlat(coord):
    return (coord[1],coord[0])

if __name__ == '__main__':

    with open("pickle/sgraph.p","rb") as f:     sgraph = pickle.load(f)

    path = "(33.9368438721,-84.5201339722) (33.9368438721,-84.5203018188) (33.9366035461,-84.5205841064) (33.9362106323,-84.5205154419) (33.936000824,-84.521522522) (33.9363174438,-84.5234527588) (33.9369430542,-84.5237884521) (33.9370918274,-84.5240325928) (33.9370727539,-84.5241470337) (33.9369277954,-84.5246887207) (33.9365386963,-84.5250701904) (33.9360122681,-84.525138855) (33.9357795715,-84.5253067017) (33.9354438782,-84.5260009766) (33.9347190857,-84.5278778076) (33.9349594116,-84.5287322998) (33.9350509644,-84.529083252) (33.9351387024,-84.5294189453) (33.935218811,-84.5297241211) (33.9353256226,-84.5301437378) (33.9355697632,-84.5311050415) (33.9356842041,-84.5315551758) (33.9358215332,-84.532081604) (33.9359817505,-84.5327072144) (33.9366188049,-84.5329818726) (33.9377746582,-84.5351715088) (33.9379196167,-84.5351715088) (33.9378662109,-84.5353240967) (33.9378662109,-84.5355224609) (33.9379882812,-84.5355224609) (33.9382896423,-84.5355224609) (33.9383659363,-84.5355682373) (33.9386062622,-84.5355682373) (33.9386444092,-84.5355682373) (33.938709259,-84.5356445312) (33.9387435913,-84.5357131958) (33.9387397766,-84.5360717773) (33.9387397766,-84.536239624) (33.9388923645,-84.536239624) (33.9388771057,-84.5366516113) (33.9388580322,-84.5374526978) (33.9388580322,-84.5375518799) (33.9388542175,-84.5377120972) (33.9388542175,-84.5379943848) (33.9388542175,-84.538269043) (33.9388542175,-84.5384674072) (33.9388504028,-84.5388565063) (33.9388504028,-84.5389480591) (33.9388504028,-84.5389709473) (33.9388504028,-84.5392074585) (33.9388465881,-84.5392837524) (33.9388504028,-84.5394287109) (33.9388504028,-84.5395889282) (33.9388504028,-84.5397796631) (33.9388504028,-84.5402832031) (33.9388504028,-84.5408325195) (33.9388542175,-84.5411834717) (33.9388542175,-84.541343689) (33.9388542175,-84.5417480469) (33.9388542175,-84.5419845581) (33.9388542175,-84.5423736572) (33.9388542175,-84.5424423218) (33.9388122559,-84.542678833) (33.9393539429,-84.5429763794) (33.9394760132,-84.5430374146) (33.9396591187,-84.5431365967) (33.9401321411,-84.5433883667) (33.9402542114,-84.5434570312) (33.9405403137,-84.5436096191) (33.9406852722,-84.5437088013) (33.9407997131,-84.543800354) (33.9410896301,-84.5442199707) (33.9412460327,-84.5445098877) (33.9414100647,-84.5447540283) (33.9418716431,-84.5452346802) (33.9419364929,-84.5452804565) (33.9420700073,-84.5453643799) (33.9425811768,-84.5456008911) (33.9434051514,-84.5459365845) (33.9438438416,-84.5461425781) (33.9442253113,-84.5463562012) (33.9451332092,-84.5469818115) (33.9457206726,-84.5473327637) (33.9465560913,-84.5478668213) (33.9467086792,-84.547958374) (33.9473457336,-84.5483169556) (33.947593689,-84.5485153198) (33.9479293823,-84.5486831665) (33.9484634399,-84.5489196777) (33.9486999512,-84.5489959717) (33.949344635,-84.5490646362) (33.9493637085,-84.5490646362) (33.9496002197,-84.5490646362) (33.9496231079,-84.5490646362) (33.9497375488,-84.5490570068) (33.9498748779,-84.5490570068) (33.9499359131,-84.5490570068) (33.9500045776,-84.5490570068) (33.9501190186,-84.5490570068) (33.9503631592,-84.5490646362) (33.9504356384,-84.5490570068) (33.9506378174,-84.5490570068) (33.9508857727,-84.5490493774) (33.9510688782,-84.5490493774) (33.9511375427,-84.5490493774) (33.9512023926,-84.5490493774) (33.9515113831,-84.549041748) (33.9522857666,-84.5490646362) (33.9532012939,-84.5490570068)"

    lat,lon = 33.93766,-84.52020
    scale = 13
    gmap = gmplot.GoogleMapPlotter(lat,lon,scale)
    edges = sgraph.edges.keys()

    colors = ['black','blue','green','yellow','orange','red']

    # this part draws the map to html
    for edge in edges:
        x,y,name,length = sgraph.edges[edge]
        pair = (x,y)
        xlat,xlon = sgraph.nodes[x]
        ylat,ylon = sgraph.nodes[y]
        lats = [xlat,ylat]
        lons = [xlon,ylon]

        width = 2
        color = 'black'
        gmap.plot(lats,lons,color,edge_width=width)
    gmap.draw("maps/example.html")



    path = path.strip().split(" ")
    path = [ map(float,x.strip("()").split(",")) for x in path ]
    path = [ tuple(x) for x in path ]

    color = "red"
    m = staticmap.StaticMap(1024,1024,64)
    last = None
    for node in path:
        if last is None:
            last = node
            continue
        xlat,xlon = last
        ylat,ylon = node
        lats = [xlat,ylat]
        lons = [xlon,ylon]

        line = [ list(reversed(last)), list(reversed(node)) ]
        line = staticmap.Line(line,'red',10)
        m.add_line(line)
        last = node
    #line = [ lonlat(box[0]), lonlat(box[1]) ]
    #line = staticmap.Line(line,'white',0)
    #m.add_line(line)
    image = m.render()
    image.save("maps/path.png")
