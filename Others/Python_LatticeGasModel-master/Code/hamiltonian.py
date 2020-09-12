import numpy as np

eps = 1.3500000   # epsilon/T in kB (Suri, Geisler)
delta_mu = 0.0    # 0 at coex,(Suri, Geisler 0.00034 slightly below coex)
mu = -3.00 * eps + delta_mu
mu_by_eps = -3.0 + delta_mu / eps

# box_dim (in A^3) = box size in x y and z dimensions
NX = NY = 30
NZ = 50
NB = np.array([NX, NY, NZ])

# periodic boundary criteria, 1 means periodic, 0 reflective
pbc = np.array([1, 1, 1])


def get_deltaH(n, i, j, k, NB):
    if i == NB[0] - 1:
        ip = (1 - pbc[0]) * (NB[0] - 1)  # taking care of X-edges
    else:
        ip = i+1

    if i == 0:
        im = (pbc[0]) * (NB[0] - 1)
    else:
        im = i-1

    if j == NB[1] - 1:
        jp = (1 - pbc[1]) * (NB[1] - 1)  # taking care of Y-edges
    else:
        jp = j+1

    if j == 0:
        jm = (pbc[1])*(NB[1]-1)
    else:
        jm = j-1

    if k == NB[2] - 1:
        kp = (1 - pbc[2]) * (NB[2] - 1)    # taking care of Z-edges
    else:
        kp = k+1

    if k == 0:
        km = (pbc[2]) * (NB[2] - 1)
    else:
        km = k-1

    # Calculating cost of changing n(i,j,k) to 1-n(i,j,k)
    DH = -eps*((1.0 - 2.0*n[i, j, k]) *
               (n[im, j, k] + n[i, jm, k] + n[i, j, km] +
                n[ip, j, k] + n[i, jp, k] + n[i, j, kp]) +
               mu_by_eps * (1.0 - 2.0*n[i, j, k]))
    # print(DH)
    return DH


# This function is to generate the LG hamiltonian based on molecular density,n


def get_hamiltonian(n, NB):
    NN = 0.0
    TN = 0.0
    for i in range(0, NB[0]):
        for j in range(0, NB[1]):
            for k in range(0, NB[2]):
                TN += n[i, j, k]
                if i == NB[0]-1:
                    ip = (1-pbc[0])*(NB[0]-1)
                else:
                    ip = i+1

                if j == NB[1]-1:
                    jp = (1-pbc[1])*(NB[1]-1)
                else:
                    jp = j+1

                if k == NB[2]-1:
                    kp = (1-pbc[2])*(NB[2]-1)
                else:
                    kp = k+1

                NN += n[i, j, k]*(n[ip, j, k]+n[i, jp, k]+n[i, j, kp])

    # hamiltonian
    H = -eps * (NN + mu_by_eps * TN)
    # print, H, NN, sum(n)
    return H
