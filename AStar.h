#ifndef AStar_h
#define AStar_h

#include <stdlib.h>

typedef struct __ASNeighborList *ASNeighborList;
typedef struct __ASPath *ASPath;

typedef struct {
    size_t  nodeSize;                                                                            
    void    (*nodeNeighbors)(ASNeighborList neighbors, void *node, void *context);                  
    float   (*pathCostHeuristic)(void *fromNode, void *toNode, void *context);                     
    int     (*earlyExit)(size_t visitedCount, void *visitingNode, void *goalNode, void *context);  
    int     (*nodeComparator)(void *node1, void *node2, void *context);                             
} ASPathNodeSource;

void ASNeighborListAdd(ASNeighborList neighbors, void *node, float edgeCost);
ASPath ASPathCreate(const ASPathNodeSource *nodeSource, void *context, void *startNode, void *goalNode);
mory
void ASPathDestroy(ASPath path);

ASPath ASPathCopy(ASPath path);
float ASPathGetCost(ASPath path);
size_t ASPathGetCount(ASPath path);
void *ASPathGetNode(ASPath path, size_t index);
#endif
