#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 28 20:31:17 2018

@author: daniel
"""

from numpy import*
import numpy as np
import General_ODE as Solve
from matplotlib import pyplot as plt
from matplotlib import animation


### Set Constants
m1 = 2.
m2 = 2.
M = 10.
l = 100.
l0 = 5.
g = 9.8
k = 3.
R = 1.


# Z = X[0], z1 = X[1], Z'=X[2], z1'=X[3]

def FM(t, X):
    return - (g*M*(m1+m2) + 4.*g*m1*m2 + k*l0*(m1+m2) + k*(m1+m2)*X[0])/(M*m1 + M*m2 + 4.*m1*m2)
    
def F1(t, X):
    return - ((m1+m2)*M*g + 4.*m1*m2*g + 2.*k*l0*m2 + 2.* k * m2 * X[0])/(M*m1 + M*m2 + 4.*m1*m2)


IC = Solve.IC([-l0, -50.], [0., 0.])


N = 1000
sol = Solve.IC_ODE(2, [FM, F1], 0., 50., IC, 'self_define', N)
t = Solve.IC_ODE(2, [FM, F1], 0., 50., IC, 'time', N)
Z = sol[0]
z1 = sol[1]

#plt.plot(t, Z)

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(-1.5, 1.5), ylim=(-200., 10.))
#plt.axes().set_aspect('equal')
line, = ax.plot([], [], '-o', lw=2)
line1, = ax.plot([], [], '-o', lw=2)
line2, = ax.plot([], [], '-o', lw=2)
Hline, = ax.plot([], [], '--', lw=1, color = 'gray')


# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    line1.set_data([], [])
    line2.set_data([], [])
    Hline.set_data([], [])
    return line, line1, line2, Hline,

    
def animate(i):
    
    line.set_data([0., 0.], [0., Z[i]])
    line1.set_data([-R, -R], [Z[i], z1[i]])
    line2.set_data([R, R], [Z[i], 2.*Z[i] - z1[i] - l])
    Hline.set_data([-R, R], [Z[i], Z[i]])
    
    return line, line1, line2, Hline,


plt.grid()
# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames = N, interval = 10, blit=True)

plt.show()
