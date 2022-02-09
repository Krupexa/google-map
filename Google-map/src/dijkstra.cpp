#include <unordered_map>
#include <unordered_set>
#include "graph.h"

typedef std::unordered_set<Graph::Node*>::const_iterator set_iter;
typedef std::unordered_map<Graph::Node*,int>::const_iterator map_iter;

Graph::Node* find_closest_open_node(
                   std::unordered_map<Graph::Node*,int> &distances,
                   std::unordered_set<Graph::Node*> &open) {
  Graph::Node* closest = nullptr;
  int closest_distance = 1024*1024; // just a large number (hack)

  set_iter it = open.begin();
  for ( ; it != open.end(); it++) {
    Graph::Node* node = *it;
    int node_distance = distances[node];
    if (node_distance < closest_distance) {
      closest_distance = node_distance;
      closest = node;
    }
  }
  return closest;
}

LinkedList::List<Graph::Node*>* 
extract_path(Graph::Node* t, 
    std::unordered_map<Graph::Node*,Graph::Node*> back_pointer) {
  Graph::Node* ptr = t;
  LinkedList::List<Graph::Node*>* path = 
    new LinkedList::List<Graph::Node*>;
  while ( ptr != nullptr ) {
    path->insert(ptr);
    ptr = back_pointer[ptr];
  }
  return path;
}

/*
 * Given a starting node s and ending node t and a map, return an
 * array containing the edges of the shortest path from s to t.  If
 * 
 *   x_1, x_2, ..., x_n 
 * 
 * are the nodes (intersections) of the shortest path, then the
 * returned list of edges (streets) has the form 
 *
 * (x_1,x_2), (x_2,x_3), (x_3,x_4), ..., (x_{n-1},x_n).
 *
 * That is the edges are in sequence, starting from s and ending at t.
 */
Graph::Path
find_shortest_path(Graph::Node* s, Graph::Node* t, 
                   Graph::UndirectedGraph* map) {

  std::unordered_map<Graph::Node*,int> distances;
                                       // map from node to shortest
                                       // distance to node found so far
  std::unordered_set<Graph::Node*> open;
                                       // contains all nodes that we
                                       // are still searching the
                                       // shortest path for
  std::unordered_set<Graph::Node*> closed;
                                       // contains all nodes that we
                                       // already found the shortest
                                       // path for
  std::unordered_map<Graph::Node*,Graph::Node*> back_pointer;
                                       // map from node to last node
                                       // used to reach it
  
  LinkedList::List<Graph::Node *> *nodes = map->get_nodes();
  LinkedList::Iterator<Graph::Node *> it = nodes->begin();

  for(; it!= nodes->end(); it++)
    {
        Graph::Node *node = *it;
        distances[node] = 1024*1024;
        open.insert(node);
    }
    
  distances[s] = 0;          // distance to start is 0 meters
  back_pointer[s] = nullptr; // no node was visited before start
  open.insert(s);            // set to closed
  
  
  while ( true ) {
    Graph::Node* closest = find_closest_open_node(distances,open);
    
    if (closest == t)
    {    break;
        
    }
    
      LinkedList::List<Graph::Edge *> *edges = closest ->get_incident();
      LinkedList::Iterator<Graph::Edge *> iter = edges->begin();
      open.erase(closest);
      closed.insert(closest);
      
      for (; iter != edges->end(); iter++)
      {
          Graph:: Edge *edge = *iter;
          
          if (closed.find(edge->get_x()) != closed.end() && open.find(edge -> get_y()) != open.end())
          {
              distances[edge->get_y()] = std::min(distances[edge->get_y()], distances[edge->get_x()] + edge->get_weight());
                       back_pointer[edge->get_y()] = edge->get_x();
          }
           
          else if (closed.find(edge->get_y()) != closed.end() && open.find(edge -> get_x()) != open.end())
         {
            distances[edge->get_x()] = std::min(distances[edge->get_x()], distances[edge->get_y()] + edge->get_weight());
            back_pointer[edge->get_x()] = edge->get_y();
             
         }
      }
      
  }

  LinkedList::List<Graph::Node*>* path = extract_path(t,back_pointer);
  int distance = distances[t];
  return Graph::Path(path,distance);
}
