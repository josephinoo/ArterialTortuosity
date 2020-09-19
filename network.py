import matplotlib.pyplot as plt
import math
import numpy as np
from visualation import*
import math 
class Graph:

    def __init__(self, row, col, g):
        self.ROW = row
        self.COL = col
        self.graph = g

    # A function to check if a given cell
    # (row, col) can be included in DFS
    def isSafe(self, i, j, visited):
        # row number is in range, column number
        # is in range and value is 1
        # and not yet visited
        return (i >= 0 and i < self.ROW and
                j >= 0 and j < self.COL and
                not visited[i][j] and self.graph[i][j])


    # A utility function to do DFS for a 2D
    # boolean matrix. It only considers
    # the 8 neighbours as adjacent vertices
    def DFS(self, i, j, visited):

        # These arrays are used to get row and
        # column numbers of 8 neighbours
        # of a given cell
        rowNbr = [-1, -1, -1,  0, 0,  1, 1, 1];
        colNbr = [-1,  0,  1, -1, 1, -1, 0, 1];

        # Mark this cell as visited
        visited[i][j] = True

        # Recur for all connected neighbours
        for k in range(8):
            if self.isSafe(i + rowNbr[k], j + colNbr[k], visited):
                self.DFS(i + rowNbr[k], j + colNbr[k], visited)


    # The main function that returns
    # count of nodes or paths deads in a given boolean
    # 2D matrix
    def countPaths(self):
        # Make a bool array to mark visited cells.
        # Initially all cells are unvisited
        visited = [[False for j in range(self.COL)]for i in range(self.ROW)]

        # Initialize count as 0 and travese
        # through the all cells of
        # given matrix
        processing=[]
        nodes_dead=[]
        delete_pores_path=[]
        count = 0
        for i in range(self.ROW):
            for j in range(self.COL):
                # If a cell with value 1 is not visited yet,
                # then new island found
                if visited[i][j] == False and self.graph[i][j] == 1:
                    # Visit all cells in this island
                    # and increment island count
                    self.DFS(i, j, visited)
                    matrix=np.array(visited,dtype=int)
                    matrix=np.logical_not(matrix)
                    matrix=np.array(matrix,dtype=int)
                    processing.append(matrix)
                    count += 1
                    
                    "Agregar los caminos muertos"
                    if (len(delete_pores_path)==0):
                        new_g=(np.array(matrix-1)*-1)
                        list_n=[list(x) for x in new_g]
                        delete_pores_path.append(list_n)
                  
                    else:
                        size=len(delete_pores_path)
                        rest=np.array(matrix)-np.array(delete_pores_path[size-1])
                        new_g=(np.array(rest-1)*-1)
                        rest=[list(agg_row) for agg_row in new_g]
                        
                        delete_pores_path.append(rest)
                        
                    agg=(np.array(matrix-1)*-1)
                    nodes_dead.append(extract_pores(agg))
                    
                    
        if (len(processing)%2==0):
            half=int(len(processing))
        else:
            half=int(len(processing))+1
       
        fig = plt.figure(figsize=(10, 10))
        
        for  process in range(len(processing)):
            ax=fig.add_subplot(half/2, half/2, process+1)
            plt.title("Dead pore :"+str(process+1))
            plt.axis(False)
            ax.imshow(processing[process])
        return processing