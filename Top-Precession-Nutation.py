# -*- coding: utf-8 -*-
"""
Created on Sun May 21 22:46:13 2017

@author: DChung
"""

# from vpython import*
from numpy import sin, cos, radians, pi, tan, array
import numpy as np
import General_ODE as Solve
import scipy.constants as const
import matplotlib.pyplot as plt
from matplotlib import animation
# import mpl_toolkits.mplot3d.axes3d as p3
# from PIL import Image 
# from Animate import animate

g = const.g * 10


# Dimension of the Top (Cone)
M = 1.
H = 0.05
R = 0.05

h = H/3. # Center of Mass of the Top
I1 = 0.6*M*(H**2 + 0.25*R**2) # Ix = Iy
I3 = 0.3*M*R**2 # Iz


# Set Differential Equations
# theta = X[0], phi = X[1], psi = X[2]
# v_theta = X[3], v_phi = X[4], v_psi = X[5]

def F_theta(t, X):
    return (X[4]**2 * sin(X[0])*cos(X[0])) - (I3/I1)*(X[4]*cos(X[0]) + X[5])*X[4]*sin(X[0]) + M*g*h*sin(X[0])/I1

def F_phi(t, X):
    return -(I3/I1)*X[3]*(X[4]*cos(X[0]) - X[5])/sin(X[0]) - 2*(1 - I3/I1)*X[3]*X[4]/tan(X[0])

def F_psi(t, X):
    return X[4]*X[3]*sin(X[0]) - F_phi(t, X)*cos(X[0])


F = [F_theta, F_phi, F_psi]


# Initial Conditions
theta = radians(30.)
phi = radians(0.)
psi = radians(0.)
theta_dot = 0.
phi_dot = 0.
psi_dot = - 2 * pi * 10.

IC = Solve.IC([theta, phi, psi], [theta_dot, phi_dot, psi_dot])
#IC = Solve.IC([theta, phi, psi], [2.*pi*0., 2.*pi*0, 2.*pi*80.])


# Solve the ODE
N = 10000
sol = Solve.IC_ODE(2, F, 0., 50., IC, 'self_define', N)

print(np.sin(sol[0]))

x = H * sin(sol[0]) * cos(sol[1])
y = H * sin(sol[0]) * sin(sol[1])
z = H * cos(sol[0])

theta = sol[0]
phi = sol[1]
psi = sol[2]
w = psi[1]-psi[0]
print (w)


# a = animate()

# a.setX(x)
# a.setY(y)
# a.setZ(z)
# a.setSpeed(2)
# a.show3d()

"""
plot 3d animate
"""

fig = plt.figure()
ax = fig.add_subplot(projection = "3d")
line = [ax.plot([], [], [])[0] for _ in range(2)]

traj = [x, y, z]

def update_lines(num, traj, line):
    
    # NOTE: there is no .set_data() for 3 dim data...
    line[0].set_data(array([0, traj[0][num]]), array([0, traj[1][num]]))
    line[0].set_3d_properties(array([0, traj[2][num]]))

    line[1].set_data(traj[0][:num], traj[1][:num])
    line[1].set_3d_properties(traj[2][:num])

    return line

ax.set(xlim3d=(min(x), max(x)), xlabel='X')
ax.set(ylim3d=(min(y), max(y)), ylabel='Y')
ax.set(zlim3d=(0, max(z)), zlabel='Z')

ani = animation.FuncAnimation(fig, update_lines, N, fargs=(traj, line), interval=100)

plt.show()

"""
Old fancy stuff that doesn't work anymore
"""

# ### new axis object
# Xaxis = arrow(pos=(0,0,0),axis=(0.5,0,0), shaftwidth=0.05)
# Xaxis.color = (1,0,0)
# Yaxis = arrow(pos=(0,0,0),axis=(0,0.5,0), shaftwidth=0.05)
# Yaxis.color = (0,1,0)
# Zaxis = arrow(pos=(0,0,0),axis=(0,0,0.5), shaftwidth=0.05)
# Zaxis.color = (0,0,1)
 
# ### new row
# r = 5
# phi = np.deg2rad(0)
# theta = np.deg2rad(30)

# rod = cylinder(pos=(0,0,0),axis=(x[0],y[0],-z[0]), radius=0.05,material = materials.wood)

# ### new yellow texture
# name = "flower"
# width = 128 # must be power of 2
# height = 128 # must be power of 2
# im = Image.open('1'+".jpg")
# tex = materials.texture(data=im, mapping="rectangular")
# ### new yellow object
# yellow = cylinder(make_trail=True,pos=(50*x[0],50*y[0],50*z[0]),axis=(x[0],y[0],-z[0]), radius=0.5,material=tex)

# ### interval
# c = 1

# ### run
# for i in range(len(x)):
#     rod.axis = (50*x[c*i],50*y[c*i],50*z[c*i])
#     rod.rotate(angle=w)
#     yellow.axis = (x[c*i],y[c*i],z[c*i])
#     yellow.pos = (50*x[c*i],50*y[c*i],50*z[c*i])
#     yellow.rotate(angle=w)
#     sleep(0.01)



























