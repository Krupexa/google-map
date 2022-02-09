#include <iostream>
#include <string>
#include "graph.h"

#ifndef MAP_H_
#define MAP_H_

namespace Map {

class Intersection : public Graph::Node {
 public:
  Intersection(int id, float lat, float lon) : Graph::Node(id) {
    this->id = id;
    this->lat = lat;
    this->lon = lon;
  }
  virtual ~Intersection() {}
  float get_lat() { return this->lat; }
  float get_lon() { return this->lon; }

 protected:
  float lat;
  float lon;
};

class Street : public Graph::Edge {
 public:
  // length is in meters
  Street(int id, Intersection* x, Intersection* y, 
         std::string name, int length) : Graph::Edge(id,x,y,length) {
    this->name = name;
  }
  virtual ~Street() { }

  std::string get_name() { return this->name; }
  int get_length() { return this->weight; } // in meters
  unsigned int hash() { return (unsigned int)this->id; }

protected:
  std::string name;
  Intersection* x;
  Intersection* y;
};

class Map : public Graph::UndirectedGraph {
 public:
  Map() {}

  virtual ~Map() { }

  Intersection* add_intersection(int id, float lat, float lon) {
    Intersection* intersection = new Intersection(id,lat,lon);
    this->add_node(intersection);
    return intersection;
  }

  Street* add_street(int id, Intersection* x, Intersection* y, 
                  std::string name, int length) {
    Street* street = new Street(id,x,y,name,length);
    this->add_edge(street);
    return street;
  }

  void print_nodes() {
    for (LinkedList::Iterator<Graph::Node*> it = this->nodes.begin(); 
         it != this->nodes.end(); it++) {
      Intersection* node = (Intersection*)*it;
      std::cout << node->get_id() << ": (" << 
        node->get_lat() << "," << node->get_lon() << ")";
      std::cout << std::endl;
    }
  }

  void print_edges() {
    for (LinkedList::Iterator<Graph::Edge*> it = this->edges.begin(); 
         it != this->edges.end(); it++) {
      Street* edge = (Street*)*it;
      std::cout << edge->get_id() << ": " << edge->get_name() << " (" << 
        edge->get_x()->get_id() << "," << edge->get_x()->get_id() << ")" <<
        " length: " << edge->get_length() << " meters";
      std::cout << std::endl;

    }
  }

  void print() {
    print_nodes();
    print_edges();
  }

 private:

};

} // END NAMESPACE MAP

#endif // MAP_H_
