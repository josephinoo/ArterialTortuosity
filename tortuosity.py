import numpy as np
from Astar import*
import math


def path_star(matrix):
    path_star = np.array(matrix)
    path_star = list(path_star[:, 0])
    path_star_new = []
    for count, element in enumerate(path_star):
        if element == 0:
            path_star_new.append((count, 0))

    return path_star_new


def path_end(matrix):
    path_end = np.array(matrix)
    path_end = list(path_end[:, -1])
    tath = np.array(matrix).shape[1]-1

    path_end_new = []
    for count, element in enumerate(path_end):
        if element == 0:
            path_end_new.append((count, tath))
    return path_end_new


def geometric_tortuosity(maze):
    """
    The geometric tortuosity of a porous medium returns
    :param maze:
    :return geometric tortuosity:
    """
    path_star_list = path_star(maze)
    path_end_list = path_end(maze)

    total_caminos = []
    total_paths = len(path_end(maze))*len(path_star(maze))
    unit_caminos = 0
    array_path = np.array(maze)
    line = (array_path.shape)[1]
    for star in path_star_list:
        caminos = []
        for end in path_end_list:

            path = astar(maze, star, end)
            result = 0
            for i in range(len(path)-1):
                add = math.sqrt((path[i][0]-path[i+1][0])
                                ** 2 + (path[i][1]-path[i+1][1])**2)
                result += add
            caminos.append(result)
            unit_caminos += 1

        total_caminos.append(min(caminos))

    valor = (np.mean(np.array(total_caminos)))
    geometric_tortusity = valor/(int(line)-1)
    return geometric_tortusity


def yes_node(graph, singular):
    """"
    Verifier to Choose Nodes
    :param graph:
    :param singular:

    """

    graph_array = np.array(graph)
    start = []
    end = []
    for elem in range(graph_array.shape[0]):
        start.append((elem, 0))
        end.append((elem, graph_array.shape[1]-1))
    verificador_start = path_star(singular)
    verificador_end = path_end(singular)
    x = False
    y = False
    for test in verificador_start:
        if test not in start:
            x = False

        else:
            x = True
    for test in verificador_end:
        if test not in end:
            y = False
        else:
            y = True
    if x and y:
        return "free_path"
    if x == True and y == False:
        return "endless_road"
    if x == False and y == True:
        return "end_node_without_start"
    if x == False and y == False:
        return "dead_node"


def type_porosity(porosity):

    if porosity == "free_path" or porosity == "endless_road":
        return "open_porosity"
    else:
        return "closed_porosity"
