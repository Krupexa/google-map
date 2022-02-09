#include "linked_list.h"

#ifndef GRAPH_H_
#define GRAPH_H_

namespace Graph {

/****************************************
 * NODE
 ****************************************/

class Edge; // forward declaration

class Node {
 public:
  Node() {
    this->id = 0;
    this->neighbor_count = 0;
  }

  Node(int id) {
    this->id = id;
    this->neighbor_count = 0;
  }

  virtual ~Node() {}

  void add_incident(Edge* edge) {
    Node* nbr = this->get_neighbor_on_edge(edge);
    this->incident.insert(edge);
    this->neighbors.insert(nbr);
    this->neighbor_count++;
  }

  Node* get_neighbor_on_edge(Edge* edge); // forward declaration
  int get_id() { return id; }
  int get_neighbor_count() { return this->neighbor_count; }
  LinkedList::List<Node*>* get_neighbors() { return &this->neighbors; }
  LinkedList::List<Edge*>* get_incident() { return &this->incident; }
  unsigned int hash() { return (unsigned int)this->id; }

 protected:
  int id;
  int neighbor_count;
  LinkedList::List<Node*> neighbors; // neighboring nodes
  LinkedList::List<Edge*> incident;  // incident edges
};

/****************************************
 * EDGE
 ****************************************/

class Edge {
 public:
  Edge(int id, Node* x, Node* y, int weight=1) {
    this->id = id;
    if ( x->get_id() < y->get_id() ) {
      // let x be the one with the smaller ID.
      // do this so that there is one unique edge for each (x,y) pair.
      this->x = x;
      this->y = y;
    } else {
      this->x = y;
      this->y = x;
    }
    this->weight = weight;
  }
  virtual ~Edge() {}

  Node* get_x() { return this->x; }
  Node* get_y() { return this->y; }
  int get_id() { return this->id; }
  int get_weight() { return this->weight; }
  unsigned int hash() { return (unsigned int)this->id; }

  Node* get_neighbor_on_edge(Node* node) {
    return node == this->x ? this->y : this->x;
  }

 protected:
  int id;
  Node* x;
  Node* y;
  int weight;
};

/****************************************
 * GRAPH
 ****************************************/

class UndirectedGraph {
  /*
   * undirected graph
   */

 public:
  UndirectedGraph() {
    this->node_count = 0;
    this->edge_count = 0;
  }

  virtual ~UndirectedGraph() {
    for (LinkedList::Iterator<Graph::Node*> it = this->nodes.begin(); 
         it != this->nodes.end(); it++) {
      Graph::Node* node = *it;
      delete node;
    }

    for (LinkedList::Iterator<Graph::Edge*> it = this->edges.begin(); 
         it != this->edges.end(); it++) {
      Graph::Edge* edge = *it;
      delete edge;
    }
  }

  Node* add_node() {
    int id = this->node_count;
    Node* node = new Node(id);
    this->add_node(node);
    return node;
  }

  Edge* add_edge(Node* x, Node* y, int weight=1) {
    int id = this->edge_count;
    Edge* edge = new Edge(id,x,y,weight);
    this->add_edge(edge);
    return edge;
  }

  int get_node_count() { return this->node_count; }
  int get_edge_count() { return this->edge_count; }
  LinkedList::List<Node*>* get_nodes() { return &this->nodes; }
  LinkedList::List<Edge*>* get_edges() { return &this->edges; }

 protected:
  void add_node(Node* node) {
    this->nodes.insert(node);
    this->node_count++;
  }

  void add_edge(Edge* edge) {
    edge->get_x()->add_incident(edge);
    edge->get_y()->add_incident(edge);
    this->edges.insert(edge);
    this->edge_count++;
  }

  LinkedList::List<Node*> nodes;
  LinkedList::List<Edge*> edges;
  int node_count;
  int edge_count;
};

struct Path {
  Path(LinkedList::List<Node*>* path, int length) {
    this->path = path;
    this->length = length;
  }

  ~Path() {
    delete this->path;
  }

  LinkedList::List<Node*>* path;
  int length;
};

} // END NAMESPACE GRAPH


#endif // GRAPH_H_
