
import matplotlib.pyplot as plt
import math
import numpy as np
import porespy as ps


def toList(array):
    """One-of-an-list converter"""
    list_new=[list(agg_row) for agg_row in array]
    return list_new

def extract_pores(graph):
    """"Extracts dead nodes or dead roads from the porous medium"""
    row = len(graph)
    col = len(graph[0])
    row_max=[]
    col_max=[]
    nodes=[]
    for i in range(row):
        for j in range(col):
            if graph[i][j]==1:
                nodes.append((i,j))
                row_max.append(i)
                col_max.append(j)
  
    #col_maxabs
    minimo=min(col_max)
    maximo=max(col_max)
    #row max
    minf=min(row_max)
    maxf=max(row_max)
    grap=np.array(graph)
    new_graph=grap[minf:maxf+1,minimo:maximo+1]
    new_graph=toList(new_graph)
    

    
    return new_graph

def searchPathVisualation(tot):
    """"Visualize the dead nodes or paths that you find respecting the size of the porous medium"""
    if (len(tot) % 2 == 0):
        half = int(len(tot))
    else:
        half = int(len(tot))+1

    fig = plt.figure(figsize=(10, 10))
    groups = []
    for process in range(len(tot)):
        ax = fig.add_subplot(half/2, half/2, process+1)
        plt.title("Path search:" + str(process+1))
        plt.axis()
        nw = np.array(tot[process])
        if nw.sum() == nw.size:
            ax.imshow(nw, cmap='gray_r')
        else:
            ax.imshow(nw, cmap='gray')
        groups.append(nw)
    return groups


def visualation_paths_unit(pathsNode):
    """View dead roads or individually dead nodes"""
    groups = []
    for proces in pathsNode:
        groups.append(extract_pores(proces))
    searchPathVisualation(groups)
    return groups

def convert_individual_paths(graph):
    """Converts individual paths of the dead nodes of the porous medium"""
    total=[]
    total.append(toList((graph[0]-1)*-1))
    for i  in range(len(graph)-1):
        rest1=np.array((graph[i]-1)*-1)
        rest2=np.array((graph[i+1]-1)*-1)
        rs=rest2-rest1
        total.append(toList(rs))
    return total
porosidad=0.75

def porous_medium(POROSITY,SIZE):

    BLOBNESS=0.5
    im=ps.generators.blobs([SIZE,SIZE],POROSITY,BLOBNESS)
    matrix=np.logical_not(np.array(im,dtype=int))
    matrix=np.array(matrix,dtype=int)
    plt.axis(True )
    plt.imshow(im,cmap='gray')
    return matrix
