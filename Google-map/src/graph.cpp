#include "graph.h"

Graph::Node* Graph::Node::get_neighbor_on_edge(Edge* edge) { 
  return edge->get_neighbor_on_edge(this);
}
