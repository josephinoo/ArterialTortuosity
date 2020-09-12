# get cell indices for location of solute or probe volume
import numpy as np


def get_vol_index(nv, loc):
    tmp = 0
    index = np.zeros((nv[0] * nv[1] * nv[2], 3), dtype=np.int)
    for i in range(0, nv[0]):
        for j in range(0, nv[1]):
            for k in range(0, nv[2]):
                index[tmp, ] = [loc[0] + i, loc[1] + j, loc[2] + k]
                tmp += 1
    return index


# get number of waters in probe volume
def get_nwater_probe(n, probe_index):
    Nwat_probe = 0.0
    for i in range(probe_index[0][0], probe_index[-1][0] + 1):
        for j in range(probe_index[0][1], probe_index[-1][1] + 1):
            for k in range(probe_index[0][2], probe_index[-1][2] + 1):
                Nwat_probe += n[i][j][k]  # *rhol*dx**3

    return Nwat_probe


def inGivenVolume(i, j, k, index):
    if (i >= index[0][0]) and (i <= index[-1][0] + 1) and \
            (j >= index[0][1]) and (j <= index[-1][1] + 1) and \
            (k >= index[0][2]) and (k <= index[-1][2] + 1):
        truth = 1
    else:
        truth = 0
    return truth
