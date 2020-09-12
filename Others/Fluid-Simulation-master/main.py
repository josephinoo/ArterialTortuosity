"""
https://thecodingtrain.com/CodingChallenges/132-fluid-simulation.html
http://www.dgp.toronto.edu/people/stam/reality/Research/pdf/GDC03.pdf
https://mikeash.com/pyblog/fluid-simulation-for-dummies.html
"""

import numpy as np
import cv2
from random import random
from fluid import Fluid

ix = 0
iy = 0

def grayscale():
    fluid = Fluid([128, 128], 0.002, diff = 0.0, visc = 0.0)
    # fluid = Fluid(128, 0.002, diff = 0.0001, visc = 0.000005)

    cx = fluid.size[1]//2
    cy = fluid.size[0]//2
    q1x = cx//2
    q3x = cx + q1x
    w = 4

    cv2.namedWindow('dye')
    def add_dye(event, x, y, flags, param):
        global ix, iy
        if event == cv2.EVENT_MOUSEMOVE:
            x = x//4
            y = y//4
            c = 5
            fluid.v[y - w:y + w, x - w:x + w] = [c*(y - iy), c*(x - ix)]
        ix = x
        iy = y
    cv2.setMouseCallback('dye', add_dye)

    # t = 0

    fluid.d[:,:] = 127

    while True:
        # fluid.d[cx - w:cx + w, cx - w:cx + w] = 200 + 55*random()
        # fluid.v[cx - w:cx + w, cx - w:cx + w] = np.sin(np.array([t, t + 3.14/2]))*20.0

        # fluid.d[cx - w:cx + w, q1x - w:q1x + w] = 200 + 55*random()
        # fluid.v[cx - w:cx + w, q1x - w:q1x + w] = np.sin(np.array([t, t + 3.14/2]))*20.0
        # fluid.d[cx - w:cx + w, q3x - w:q3x + w] = 200 + 55*random()
        # fluid.v[cx - w:cx + w, q3x - w:q3x + w] = np.sin(np.array([-t, -t - 3.14/2]))*20.0

        fluid.d[cy - w:cy + w, q1x - w:q1x + w] = 200 + 55*random()
        fluid.v[cy - w:cy + w, q1x - w:q1x + w] = [0, 15*random()]
        fluid.d[cy - w:cy + w, q3x - w:q3x + w] = 55*random()
        fluid.v[cy - w:cy + w, q3x - w:q3x + w] = [0, -15*random()]

        fluid.step()
        # fluid.d = np.clip(fluid.d - 1.0, 0, 255)

        # t += random()*0.03

        cv2.imshow('dye', cv2.pyrUp(cv2.pyrUp(fluid.d.astype('uint8'))))
        ch = cv2.waitKey(1)
        if ch == 27: break

    cv2.destroyAllWindows()

def color():
    fluid_r = Fluid([128, 128], 0.002, diff = 0.0, visc = 0.0)
    fluid_g = Fluid([128, 128], 0.002, diff = 0.0, visc = 0.0)
    fluid_b = Fluid([128, 128], 0.002, diff = 0.0, visc = 0.0)

    cx = fluid_r.size[1]//2
    cy = fluid_r.size[0]//2
    q1x = cx//2
    q3x = cx + q1x
    w = 4

    while True:
        velocity_right = -15*random()
        velocity_left = 15*random()
        fluid_r.d[cy - w:cy + w, q1x - w:q1x + w] = 200 + 55*random()
        fluid_r.d = np.clip(fluid_r.d - 0.5, 0, 255)
        fluid_r.v[cy - w:cy + w, q1x - w:q1x + w] = [0, velocity_left]
        fluid_r.v[cy - w:cy + w, q3x - w:q3x + w] = [0, velocity_right]

        fluid_b.d[cy - w:cy + w, q3x - w:q3x + w] = 200 + 55*random()
        fluid_b.d = np.clip(fluid_b.d - 0.5, 0, 255)
        fluid_b.v[cy - w:cy + w, q1x - w:q1x + w] = [0, velocity_left]
        fluid_b.v[cy - w:cy + w, q3x - w:q3x + w] = [0, velocity_right]

        fluid_g.d[cy - w:cy + w, cx - w:cx + w] = 200 + 55*random()
        fluid_g.d = np.clip(fluid_g.d - 0.5, 0, 255)
        fluid_g.v[cy - w:cy + w, q1x - w:q1x + w] = [0, velocity_left]
        fluid_g.v[cy - w:cy + w, q3x - w:q3x + w] = [0, velocity_right]

        fluid_r.step()
        fluid_g.step()
        fluid_b.step()

        full_color = np.dstack((fluid_b.d, fluid_g.d, fluid_r.d))

        cv2.imshow('dye', cv2.pyrUp(cv2.pyrUp(full_color.astype('uint8'))))
        ch = cv2.waitKey(1)
        if ch == 27: break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    grayscale()
