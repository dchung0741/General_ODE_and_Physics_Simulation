# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

"""



import numpy as np
from numpy import array
from matplotlib import pyplot as plt
from matplotlib import animation
import mpl_toolkits
import mpl_toolkits.mplot3d.axes3d as p3



class animate():
    
    def __init__(self):
        
        self.xData = []
        self.yData = []
        self.zData = []
    
        self.isdynamic = False

    def setX(self,x):
        
        if type(x) == np.ndarray:            
            self.xData = x
        else:
            self.xData = np.asarray(x)
            
        
    def setY(self,y):
        if type(y) == np.ndarray:            
            self.yData = y
        else:
            self.yData = np.asarray(y)
        
    def setZ(self,z):
        if type(z) == np.ndarray:            
            self.zData = z
        else:
            self.zData = np.asarray(z)
    
    def setSpeed(self,speed):
        
        if speed > 1:
            
            newx = [self.xData[0]]
            newy = [self.yData[0]]
        
            if len(self.zData) != 0:
                newz = [self.zData[0]]
            cursor = 0            
            
            for i in range(len(self.xData)):
                if int(i/speed) != cursor:
                    cursor = int(i/speed)
                    newx.append(self.xData[i])
                    newy.append(self.yData[i])
                    
                    if len(self.zData) != 0:
                        newz.append(self.zData[i])
                        
                        
            self.xData = newx
            self.yData = newy
            if len(self.zData) != 0:
                self.zData = newz
                    
        if speed < 1 and speed > 0:
            
            
            newx = []
            newy = []
        
            if self.zData != None:
                newz = []
            cursor = 0 
            
            
            for i in range(len(self.xData)):
                for _ in range(int(1/speed)):
                    newx.append(self.xData[i])
                    newy.append(self.yData[i])
                    
                    if self.zData != None:
                        newz.append(self.zData[i])
                        
            self.xData = newx
            self.yData = newy
            if self.zData != None:
                self.zData = newz
    
       
      
    def show2d(self):
        
        # check user input
        if len(self.xData) == 0:
            print ('you need to input xdata')
        
        if len(self.yData) == 0:
            print ('you need to input ydata')
            
        if len(self.yData) != len(self.xData):
            print ('len xData is not equal to  ydata')
            
        # initial
        frame = len(self.xData)
            
        
        fig = plt.figure(1)
        ax = fig.add_subplot(1, 1, 1)
        
        # rescale
        #ax.set_xlim([np.amin(self.xData) - 1. , np.amax(self.xData) + 1.])
        #ax.set_ylim([np.amin(self.yData) - 1. , np.amax(self.yData) + 1.])
        line, = ax.plot([], [], lw=2)
        
        # initialization function: plot the background of each frame
        def init():
            line.set_data([], [])
            return line,
        
        # animation function.  This is called sequentially
        def animate(i):
            line.set_data(self.xData[0:i+1], self.yData[0:i+1])
            return line,
          
        ani = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=frame, interval = 20 , blit=False)
        
        # plt.show(ani)
        plt.show()
        
        
        
    def show3d(self):
        
        # check user input        
        if len(self.xData) == 0:
            print ('you need to input xdata')
        
        if len(self.yData) == 0:
            print ('you need to input ydata')
            
        if len(self.zData) == 0:
            print ('you need to input zdata')
            
        if len(self.yData) != len(self.xData):
            print ('len xData is not equal to ydata')
            
        if len(self.yData) != len(self.zData):
            print ('len zData is not equal to ydata')
            
        
        frame = len(self.xData)        
        
        
        # initial
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        line, = ax.plot([], [], [])
        
        # rescale
        ax.set_xlim3d([np.amin(self.xData) - np.std(self.xData), np.amax(self.xData) + np.std(self.xData)])

        
        ax.set_ylim3d([np.amin(self.yData) - np.std(self.yData), np.amax(self.yData) + np.std(self.yData)])

        
        ax.set_zlim3d([np.amin(self.zData) - np.std(self.zData), np.amax(self.zData) + np.std(self.zData)])

        # initialization function: plot the background of each frame
        def init():
            line.set_data([], [])
            line.set_3d_properties(array([]))
            return line,
        
        # animation function.  This is called sequentially
        def animate(i):
            line.set_data(self.xData[0:i+1], self.yData[0:i+1])
            line.set_3d_properties(self.zData[0:i+1])
            return line,
            
        ani = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=frame, interval = 20 , blit=False)
        
        
        # plt.show(ani)
        plt.show()
        
    def dynamic2d(self,xdata,ydata):
        
        if self.isdynamic == False:
                    
            self.xDynamic = []
            self.yDynamic = []
            
            plt.ion()
            #Set up plot
            self.figure, self.ax = plt.subplots()
            self.lines, = self.ax.plot([],[])
            #Autoscale on unknown axis and known lims on the other
            self.ax.set_autoscaley_on(True)
            
            self.isdynamic = True
        
        else:
            self.xDynamic.append(xdata)
            self.yDynamic.append(ydata)
            #Update data (with the new _and_ the old points)
            self.lines.set_xdata(self.xDynamic)
            self.lines.set_ydata(self.yDynamic)
            #Need both of these in order to rescale
            self.ax.relim()
            self.ax.autoscale_view()
            #We need to draw *and* flush
            self.figure.canvas.draw()
            self.figure.canvas.flush_events()
            
    def dynamic3d(self,xdata,ydata,zdata):
        
        
            def checkMinMax(x,y,z):
                if x < self.xmin:
                    self.xmin = x 
                if x > self.xmax:
                    self.xmax = x 
                if y < self.ymin:
                    self.ymin = y 
                if y > self.ymax:
                    self.ymax = y                   
                if z < self.zmin:
                    self.zmin = z 
                if z > self.zmax:
                    self.zmax = z 
            
            if self.isdynamic == False:
                
                #initialize
                
                #set Dynamic data 
                self.xDynamic = []
                self.yDynamic = []
                self.zDynamic = []
                
                # Setting the axes properties max and min
                self.xmin = 0
                self.ymin = 0
                self.zmin = 0
                self.xmax = 0
                self.ymax = 0
                self.zmax = 0
                
                
                #Set up plot
                plt.ion()
                self.figure = plt.figure()
                self.ax = self.figure.add_subplot(111, projection='3d')
                self.lines, = self.ax.plot([],[],[])
                
                self.isdynamic = True
            
            else:
                self.xDynamic.append(xdata)
                self.yDynamic.append(ydata)
                self.zDynamic.append(zdata)
                #Update data (with the new _and_ the old points)
                self.ax.relim()
                self.lines.set_xdata(self.xDynamic)
                self.lines.set_ydata(self.yDynamic)
                self.lines.set_3d_properties(self.zDynamic)
                
                # rescale
                checkMinMax(xdata,ydata,zdata)
                self.ax.set_xlim3d([self.xmin , self.xmax])               
                self.ax.set_ylim3d([self.ymin , self.ymax])                       
                self.ax.set_zlim3d([self.zmin , self.zmax])

                
                
                #We need to draw *and* flush
                self.figure.canvas.draw()
                self.figure.canvas.flush_events()            
        



"""
a = animate()
x = np.linspace(0,100,1001)
y = np.sin(x)
z = np.cos(x)

a.setX(x)
a.setY(y)
a.setZ(z)
a.setSpeed(2)
a.show3d()

"""



































