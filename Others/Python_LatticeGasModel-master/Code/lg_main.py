#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# Written by Suruchi Fialoke 05-April 2016
# Lattice Gas Simulations using Monte Carlo Scheme
# The function lg_cuboid takes maximum MC sweeps/iternations and Nstar as input
# Incorporates Umbrella sampling to restrict number of waters
# at Nstar in defined probe volume
# import pygame as pg
# import sys
# import math

import numpy as np
import random
import datetime
import time
from hamiltonian import get_deltaH, get_hamiltonian
from getNV import *
from save_density import *


# LG Parameters
rhol = 0.03294      # waters/A^3
dx = 1.84           # dx (in A) = grid spacing for L.Gas = 1.84 A(Suri, Geisler)
dnl = rhol*dx**3    # number of waters in one grid


# box_dim (in A^3) = box size in x y and z dimensions
NX = NY = 30
NZ = 30
NB = np.array([NX, NY, NZ])
NTOT = NX*NY*NZ
box_dim = NB*dx


# if only bulk water, set isolute =0
isolute = 0
if isolute == 1:
    NS = np.array([NX, NY, 2])    	# number of cells in each dim
    NS_TOT = NS[0]*NS[1]*NS[2]

    # VSOL = NS_TOT*dx*dx*dx, sol_dim = NS*dx
    loc_sol = np.array([0, 0, 0])    # bottom left corner location of solute
    sol_index = np.zeros((NS_TOT, 3), dtype=np.int)   # indices of solute
    sol_index = get_vol_index(NS, loc_sol)   # getting indices of solute

else:
    NS_TOT = 0

# Probe volume definition (Only Cuboid)
kappa = 2.5	    # Umbrella potential kappa in Kb, test different values
Nstar = 0           # Biasing system to Nstar value
NP = np.array([6, 6, 7])   # number of cells in each dim
NP_TOT = NP[0]*NP[1]*NP[2]
# VP = NP_TOT*dx*dx*dx, probe_dim = NP*dx
loc_probe = np.array([(NX-NP[0])//2, (NY-NP[1])//2, (NZ-NP[2])//2])
probe_index = np.zeros((NP_TOT, 3), dtype=np.int)
probe_index = get_vol_index(NP, loc_probe)


def printTime():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print(st)


def Sweep(rho_prev, Nprobe_prev):
    # Starting 1 sweep...................................................
    Nprobe_tmp = Nprobe_prev
    rho_tmp = np.ones(NB)
    rho_tmp = rho_prev
    for t in range(1, NTOT-NS_TOT + 1):
        i = random.randrange(0, NX)
        j = random.randrange(0, NY)
        k = random.randrange(0, NZ)

        # Set the density to zero if coincides with solute
        if((isolute == 1) and inGivenVolume(i, j, k, sol_index)):
            rho[i][j][k] = 0

        # Else try chaning nijk -> 1-nijk
        else:
            DH = DH0 = get_deltaH(rho_tmp, i, j, k, NB)
            # if nijk also lies in the probe add Umb. potential in delta H
            if((kappa > 0) and inGivenVolume(i, j, k, probe_index)):
                D_umb = kappa*(1 - 2.0 * rho_tmp[i][j][k]) * dnl * \
                    (Nprobe_tmp + (1 - 2.0*rho_tmp[i][j][k]) * dnl/2.0 - Nstar)
                DH = DH0 + D_umb
            # if lower in energy, keep the swap
            if(DH < 0 or np.exp(-1.0 * DH) > random.random()):
                rho_tmp[i][j][k] = 1 - rho_tmp[i][j][k]
                # accepts += 1
                # If ijk additionally lies in probe volume, update nprobe
                if((kappa > 0) and inGivenVolume(i, j, k, probe_index)):
                    Nprobe_tmp += dnl * (2.0 * rho_tmp[i][j][k] - 1)
    return(rho_tmp)
    # Finishing 1 sweep.....................................................


def Main():
    # max_itern = total number of samples/iternations 1 iternation = 1 sweep
    try:
        max_itern = int(input("Please enter total number of iterations: "))
    except:
        print("That is not a number, try again..")
        quit()

    # initializing cells, n=1 if liquid
    itern = 0
    rho = rho_prev = np.ones(NB)

    # Set density to zero if coincides with solute
    if isolute == 1:
        for i in range(sol_index[0][0], sol_index[-1][0]+1):
            for j in range(sol_index[0][1], sol_index[-1][1]+1):
                for k in range(sol_index[0][2], sol_index[-1][2]+1):
                    rho[i][j][k] = 0
                    rho_prev[i][j][k] = 0

    Nwat_init = Nwat_prev = dnl*rho_prev.sum()
    Nprobe_init = Nprobe_prev = dnl*get_nwater_probe(rho_prev, probe_index)
    Hinit = Hprev = get_hamiltonian(rho_prev, NB)

    # write initial densities
    write_density_dx(itern, rho, NB)
    write_rhoz(itern, rho, NB, dx)
    f_free = open("F_Nstar"+str(Nstar)+".dat", "w")
    f_Nstar = open("Nstar"+str(Nstar)+".dat", "w")
    f_free.write("#kappa = %-8.3f and Nstar = %-8.3f\n" % (kappa, Nstar))
    f_Nstar.write("#kappa = %-8.3f and Nstar = %-8.3f\n" % (kappa, Nstar))
    f_Nstar.write("#iteration	Nprobe     Nprobe\n")
    f_Nstar.write("%d\t%-8.3f\t%-8.3f\n" % (itern, Nprobe_init, Nwat_init))
    f_free.write("#itern    N   Nprobe     H    DN        DH")
    # f_free.write("%d%-8.3f%-8.3f%-8.3f%-8.3f%-8.3f%-8.3f\n"
    # %(itern, Nwat_init, Nprobe_init, Nprobe_init,Hinit,0.0,0.0))

    

    # starting the iternations...............................................
    print("# Starting interations...")
    printTime()

    while itern < max_itern-1:
        itern += 1
        rho = Sweep(rho_prev, Nprobe_prev)
        Nwat = dnl*rho.sum()
        Hnew = get_hamiltonian(rho, NB)
        Nprobe = dnl*get_nwater_probe(rho, probe_index)

        f_Nstar.write("%d\t%-8.3f\t%-8.3f\n" % (itern, Nprobe, Nwat))
        print(itern, Nwat, Nprobe, Hnew,
              Nwat-Nwat_prev, Nprobe - Nprobe_prev, Hnew - Hprev)

        if itern % 100 == 0:
            print(itern, Nwat, Nwat_prev, Hnew, Hprev)
            printTime()
            write_density_dx(itern, rho, NB)
            write_rhoz(itern, rho, NB, dx)

        # Store new values in the old
        Hprev = Hnew
        Nwat_prev = Nwat
        Nprobe_prev = Nprobe

        # Ending the iternations................................................
    f_free.close()
    f_Nstar.close()


if __name__ == "__main__":
    Main()
