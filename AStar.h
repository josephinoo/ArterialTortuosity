#ifndef AStar_h
#define AStar_h

#include <stdlib.h>

typedef struct __ASNeighborList *ASNeighborList;
typedef struct __ASPath *ASPath;

typedef struct {
    size_t  nodeSize;                                                                               // the size of the structure being used for the nodes - important since nodes are copied into the resulting path
    void    (*nodeNeighbors)(ASNeighborList neighbors, void *node, void *context);                  // add nodes to the neighbor list if they are connected to this node
    float   (*pathCostHeuristic)(void *fromNode, void *toNode, void *context);                      // estimated cost to transition from the first node to the second node -- optional, uses 0 if not specified
    int     (*earlyExit)(size_t visitedCount, void *visitingNode, void *goalNode, void *context);   // early termination, return 1 for success, -1 for failure, 0 to continue searching -- optional
    int     (*nodeComparator)(void *node1, void *node2, void *context);                             // must return a sort order for the nodes (-1, 0, 1) -- optional, uses memcmp if not specified
} ASPathNodeSource;

// use in the nodeNeighbors callback to return neighbors
void ASNeighborListAdd(ASNeighborList neighbors, void *node, float edgeCost);

// if goalNode is NULL, it searches the entire graph and returns the cheapest deepest path
// context is optional and is simply passed through to the callback functions
// startNode and nodeSource is required
// as a path is created, the relevant nodes are copied into the path
ASPath ASPathCreate(const ASPathNodeSource *nodeSource, void *context, void *startNode, void *goalNode);

// paths created with ASPathCreate() must be destroyed or else it will leak memory
void ASPathDestroy(ASPath path);

// if you want to make a copy of a path result, this function will do the job
// you must call ASPathDestroy() with the resulting path to clean it up or it will cause a leak
ASPath ASPathCopy(ASPath path);

// fetches the total cost of the path
float ASPathGetCost(ASPath path);

// fetches the number of nodes in the path
size_t ASPathGetCount(ASPath path);

// returns a pointer to the given node in the path
void *ASPathGetNode(ASPath path, size_t index);

#endif
