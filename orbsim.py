
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 15:18:57 2018

Orbital simulator, but with arrays.
In these functions, "target" is the body being updated, while "body" stands for
every other body in the system.

@author: Alfonso Botta-Lopez
"""
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#Constants
mass_earth = 5.9723e+24
mass_sun = 1988500e+24
G = 6.67259e-11

trashBoiX = []
trashBoiY = []
trashBoiZ = []

#Array of all bodies being taken into consideration
bodyArray = ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter']

massArray = [1988500e+24, 0.3304e+24, 4.8675e+24, 5.9723e+24, 0.64171e+24, 1,898.19e+24]

#Array of positions of all bodies. Each body has x and y positions
positionArray = np.array([[0, 0], 
                          [9.990354752e+9, 4.490203572e+10], 
                          [-8.045675354e+10, 7.1226472626e+10], 
                          [0 ,-1.4709e+11], 
                          [7.993131292e+10, -1.90532962e+11],
                          [7.161041882e+11, 1.885859539e+11]])

#Array of velocities of all bodies. 
velocityArray = np.array([[0.0, 0.0], 
                          [-57572.21884, 12809.37225], 
                          [-26394.72581, -23379.17983], 
                          [30290.0, 0.0], 
                          [24436.76069, 10251.57193],
                          [-3494.030258, 13267.63553]])

#Create blank arrays. This is here because I was having problems with the array name not being found
rArray = []
aArray = []
a_totArray = []

#Use each body and the planar distance equation to find r (r being distance not radius)
#In this function, "target" most nearly means "origin".
def find_r(target):
    rArray = []
    for body in bodyArray:
        #Checks that the body being updated is not the same as
        if target == body:
            rArray.append([0, 0, 0])
        else: 
            #Grabs array values for X and Y positions of target and origin body.
            X1 = positionArray[bodyArray.index(body)][0]
            Y1 = positionArray[bodyArray.index(body)][1]
            X2 = positionArray[bodyArray.index(target)][0]
            Y2 = positionArray[bodyArray.index(target)][1]
            #Planar distance formula.
            r = math.sqrt((X2 - X1) ** 2 + (Y2 - Y1) ** 2)
            r_x = X2 - X1
            r_y = Y2 - Y1
            #For each target body, this is appended to the array. 
            rArray.append([r, r_x, r_y])
    rArray = np.array(rArray)
    return rArray

#Finds acceleration on target body from other bodies
def find_a(target):
    aArray = []
    for body in bodyArray:
        if body == target:
            aArray.append([0, 0, 0])
        else:
            #Rebuilds the distance array based on new origin planet.
            rArray = find_r(target)
            #Finds the force between the origin body and all other bodies, as well as accelerations. 
            F = -G * (massArray[bodyArray.index(body)] * massArray[bodyArray.index(target)]) / (rArray[bodyArray.index(body)][0] ** 2)
            a_tot = F / (massArray[bodyArray.index(target)])
            a_x = a_tot * ((rArray[bodyArray.index(body)][1]) / (rArray[bodyArray.index(body)][0]))
            a_y = a_tot * ((rArray[bodyArray.index(body)][2]) / (rArray[bodyArray.index(body)][0]))
            aArray.append([a_tot, a_x, a_y])
    #print aArray
    return aArray

#Finds the total x and y acclerations experienced by an object as a result of all other objects
def find_a_total(target):
    a_totArray = []
    aArray = find_a(target)
    a_x_tot = 0
    a_y_tot = 0
    for item in aArray:
        a_x_tot += item[1]
        a_y_tot += item[2]
    a_totArray.append([a_x_tot, a_y_tot])
    a_totArray = np.array(a_totArray)
    return a_totArray

"""
#Create text files for the output of each body (otherwise the output is a mess)
#This function is useless for now
def create_files():
    for body in bodyArray:
        pass
    return 0
"""

#([a_tot, a_x, a_y], [a_tot, a_x, a_y])
def update_position(target):
    #outfile = open(target, 'w')
    for counter in range(0, 4000):
        for body in bodyArray:
            if body == target:
                a_totArray = find_a_total(target)
                velocityArray[bodyArray.index(target)][0] += (a_totArray[0][0] * 86400)
                velocityArray[bodyArray.index(target)][1] += (a_totArray[0][1] * 86400)
                positionArray[bodyArray.index(target)][0] += velocityArray[bodyArray.index(target)][0] * 86400
                positionArray[bodyArray.index(target)][1] += velocityArray[bodyArray.index(target)][1] * 86400
                trashBoiX.append(positionArray[bodyArray.index(target)][0])
                trashBoiY.append(positionArray[bodyArray.index(target)][1])
                trashBoiZ.append(0)
                #print >>outfile, positionArray[bodyArray.index(target)][0], positionArray[bodyArray.index(target)][1]                
    return 0

def update_test():
    for body in bodyArray:
        update_position(body)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = trashBoiX
    y = trashBoiY
    z = trashBoiZ
    ax.scatter(x, y, z, c='r', marker='o')
    plt.show()
    return 0

update_test()
