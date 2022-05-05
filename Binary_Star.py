#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 23:05:44 2018

@author: daniel
"""

from numpy import*
import numpy as np
from numpy import inf
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation
import General_ODE as Solve
import matplotlib.pyplot as plt


############################################################################################################################################
# User Interface
############################################################################################################################################


# Initial Condition
test_case = [
    {
    'm1': 1, 'm2': 2, 'G': -2,
    'x10': 100, 'x20': -100, 'y10': 0, 'y20': 0, 'z10': 0, 'z20': 0,
    'vx10': 0, 'vx20': 0, 'vy10': -0.05, 'vy20': 0.05, 'vz10': 0, 'vz20': 0,
    'run_time': 10000, 'N': 10000, 'refresh_time': 10
    },

    {
    'm1': 1, 'm2': 50000, 'G': -1,
    'x10': 0, 'x20': 0, 'y10': 0, 'y20': -30, 'z10': 0, 'z20': 0,
    'vx10': 0, 'vx20': 10, 'vy10': 0, 'vy20': 0, 'vz10': 0, 'vz20': 0,
    'run_time': 20, 'N': 100000, 'refresh_time': 10
    }
    ]

test_case_num = 1

### Constants
m1 = test_case[test_case_num]['m1']
m2 = test_case[test_case_num]['m2']
G = test_case[test_case_num]['G']


set_speed = 10
run_time = test_case[test_case_num]['run_time']
############################################################################################################################################


### The ODEs
def F21x(t, X):
    r = ( (X[0] - X[1])**2 + (X[2] - X[3])**2 + (X[4] - X[5])**2 )**0.5
    return - G*m2*(X[1] - X[0])/r**3

def F21y(t, X):
    r = ( (X[0] - X[1])**2 + (X[2] - X[3])**2 + (X[4] - X[5])**2 )**0.5
    return - G*m2*(X[3] - X[2])/r**3

def F21z(t, X):
    r = ( (X[0] - X[1])**2 + (X[2] - X[3])**2 + (X[4] - X[5])**2 )**0.5
    return + G*m2*(X[5] - X[4])/r**3


def F12x(t, X):
    r = ( (X[0] - X[1])**2 + (X[2] - X[3])**2 + (X[4] - X[5])**2 )**0.5
    return + G*m1*(X[1] - X[0])/r**3

def F12y(t, X):
    r = ( (X[0] - X[1])**2 + (X[2] - X[3])**2 + (X[4] - X[5])**2 )**0.5
    return + G*m1*(X[3] - X[2])/r**3

def F12z(t, X):
    r = ( (X[0] - X[1])**2 + (X[2] - X[3])**2 + (X[4] - X[5])**2 )**0.5
    return + G*m1*(X[5] - X[4])/r**3


F = [F21x, F12x, F21y, F12y, F21z, F12z]

### Initial Conditions
x10 = test_case[test_case_num]['x10']
x20 = test_case[test_case_num]['x20']
y10 = test_case[test_case_num]['y10']
y20 = test_case[test_case_num]['y20']
z10 = test_case[test_case_num]['z10']
z20 = test_case[test_case_num]['z20']

vx10 = test_case[test_case_num]['vx10']
vx20 = test_case[test_case_num]['vx20']
vy10 = test_case[test_case_num]['vy10']
vy20 = test_case[test_case_num]['vy20']
vz10 = test_case[test_case_num]['vz10']
vz20 = test_case[test_case_num]['vz20']


initial_cond = [x10, x20, y10, y20, z10, z20, vx10, vx20, vy10, vy20, vz10, vz20]


###
N = test_case[test_case_num]['N']
t_int = run_time
sol = Solve.IC_ODE(2, F, 0., t_int, initial_cond, 'self_define', N)
t = Solve.IC_ODE(2, F, 0., t_int, initial_cond, 'time', N)


""" Animate """

x1 = sol[0][::set_speed]
x2 = sol[1][::set_speed]
y1 = sol[2][::set_speed]
y2 = sol[3][::set_speed]
z1 = sol[4][::set_speed]
z2 = sol[5][::set_speed]



#############################################################################################
# Animate 
#############################################################################################

Ani_3d = False

fig = plt.figure()

if Ani_3d:

    ax = fig.add_subplot(111, projection='3d') 

    star1, = ax.plot([], [], [], '-b')
    starline1, = ax.plot([], [], [], '--ob')

    star2, = ax.plot([], [], [], '-r')
    starline2, = ax.plot([], [], [], '--or')

    ax.set_xlim3d( min(list(x1)+list(x2)), max(list(x1)+list(x2)) )
    ax.set_ylim3d( min(list(y1)+list(y2)), max(list(y1)+list(y2)) )
    # ax.set_zlim3d( min(list(z1)+list(z2)), max(list(z1)+list(z2)) )

    # initialization function: plot the background of each frame (3D)
    def init():
    
        star1.set_data([], [])
        star1.set_3d_properties(array([]))
        
        starline1.set_data([], [])
        starline1.set_3d_properties(array([]))
        
        
        star2.set_data([], [])
        star2.set_3d_properties(array([]))
        
        starline2.set_data([], [])
        starline2.set_3d_properties(array([]))

        
        return star1, starline1, star2, starline2, 
    
    # Animate 3d
    def animate(i):
    
        X1 = x1[:i]
        Y1 = y1[:i]
        Z1 = z1[:i]
        
        star1.set_data(X1, Y1)
        starline1.set_data([0, x1[i]], [0, y1[i]])
        
        star1.set_3d_properties(array(Z1))
        starline1.set_3d_properties(array([0, z1[i]]))
        
        
        X2 = x2[:i]
        Y2 = y2[:i]
        Z2 = z2[:i]
        
        star2.set_data(X2, Y2)
        starline2.set_data([0, x2[i]], [0, y2[i]])
        
        star2.set_3d_properties(array(Z2))
        starline2.set_3d_properties(array([0, z2[i]]))
        
        return star1, starline1, star2, starline2,



else:

    ax = plt.axes(xlim=(min(list(x1)+list(x2)), max(list(x1)+list(x2))), ylim=(min(list(y1)+list(y2)), max(list(y1)+list(y2))))

    star1, = ax.plot([], [], '-b')
    starline1, = ax.plot([], [], '--ob')
    star2, = ax.plot([], [], '-r')
    starline2, = ax.plot([], [], '--or')

    ax.set_xlim( min(list(x1)+list(x2)), max(list(x1)+list(x2)) )
    ax.set_ylim( min(list(y1)+list(y2)), max(list(y1)+list(y2)) )

    # initialization function: plot the background of each frame (2D)
    def init():
    
        star1.set_data([], [])
        starline1.set_data([], [])
        
        star2.set_data([], [])
        starline2.set_data([], [])
        
        return star1, starline1, star2, starline2, 
    
    # Animate 2d
    def animate(i):
    
        X1 = x1[:i]
        Y1 = y1[:i]

        star1.set_data(X1, Y1)
        starline1.set_data([0, x1[i]], [0, y1[i]])


        X2 = x2[:i]
        Y2 = y2[:i]

        star2.set_data(X2, Y2)
        starline2.set_data([0, x2[i]], [0, y2[i]])

        return star1, starline1, star2, starline2,



anim = animation.FuncAnimation(fig, animate, init_func = init,
                               frames = N//set_speed, 
                               interval= test_case[test_case_num]['refresh_time'], 
                               blit = True)

plt.show()

"""
plt.plot(x1, y1)
plt.plot(x2, y2)
plt.grid()
plt.show()
"""