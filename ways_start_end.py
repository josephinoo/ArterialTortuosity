

def points_start_end_3d(maze):
    points=[]
    for row in maze:
        for column in row:
            if(column==0):
                points.append((row,column))
    return points

    
def points_start_end_2d(maze):
    points=[]
    for row in maze:
        if(row[0]==0):
            points.append((row[0],0))
    return points