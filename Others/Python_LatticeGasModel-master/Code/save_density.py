import numpy as np


# FUNCTION TO WRITE DENSITY IN .DX FILES
def write_density_dx(itern, rho, NB):

    ncubes = NB[0] * NB[1] * NB[2]
    fdat = open("rho_itern.%d.dx" % itern, 'w')
    fdat.write("#volmap for WATERS\n")
    fdat.write("object 1 class gridpositions counts %3d%3d%3d\n" % (NB[0], NB[1], NB[2]))
    fdat.write("origin%5.1f%5.1f%5.1f\n" % (0.0, 0.0, 0.0))
    fdat.write("delta%2d%2d%2d\n" % (1, 0, 0))
    fdat.write("delta%2d%2d%2d\n" % (0, 1, 0))
    fdat.write("delta%2d%2d%2d\n" % (0, 0, 1))
    fdat.write("object 2 class gridconnections counts %3d%3d%3d\n" % (NB[0], NB[1], NB[2]))
    fdat.write("object 3 class array type double rank 0 items %6d data follows\n" % ncubes)
    cubecount = 0
    rhocg = np.zeros(3)

    for i in range(0, NB[0]):
        for j in range(0, NB[1]):
            for k in range(0, NB[2]):
                rhocg[cubecount] = rho[i][j][k]
                cubecount += 1
                if cubecount >= 3:
                    cubecount = 0
                    fdat.write("%-8.3f%-8.3f%-8.3f\n" % (rhocg[0], rhocg[1], rhocg[2]))
                elif i == NB[0] - 1 and j == NB[1] - 1 and k == NB[2] - 1:
                    if cubecount == 1:
                        fdat.write("%-8.3f\n" % rhocg[0])
                    elif cubecount == 2:
                        fdat.write("%-8.3f%-8.3f\n" % (rhocg[0], rhocg[1]))

    fdat.close()


# FUNCTION to write DENSITY averaged over x and y as a function of z
def write_rhoz(itern, rho, NB, dx):
    fdat1 = open("zrho_itern.%d.dat" % itern, 'w')
    fdat1.write("#z     rhoz(avg_xy)\n")
    rhoz = np.zeros(NB[2])

    for k in range(0, NB[2]):
        for i in range(0, NB[0]):
            for j in range(0, NB[1]):
                rhoz[k] += rho[i][j][k]

        fdat1.write("%-8.3f%-8.3f\n" % (dx * (k + 0.5), rhoz[k] / NB[0] / NB[1]))

    fdat1.close()
