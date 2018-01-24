import numpy as np
import random
import math
import matplotlib.pyplot as plt

from pylab import *

def gen_sin(x, range_weight, npi, theta):
    LIGHT_NUMBER = 5
    while True:
        step = range_weight/npi/(LIGHT_NUMBER-1);
        delta = np.arange(LIGHT_NUMBER)
        delta = delta*step
        x_array = x+delta
        # print(x_array.shape)
        # print(delta.shape)
        x_array = np.reshape(x_array,[1,LIGHT_NUMBER])
        height = np.sqrt(1-x_array*x_array)
        weight = np.sin(npi*math.pi*x_array)
        # print(height.shape)
        # print(weight.shape)
        y_array = height*weight
        y_array = np.reshape(y_array,[1, LIGHT_NUMBER])
        xy_mat = np.concatenate([x_array, y_array], axis=0)
        x_min = np.min(x_array)
        x_max = np.max(x_array)
        x_range = x_max-x_min
        y_min = np.min(y_array);y_max = np.max(y_array);
        y_range = y_max-y_min
        if y_range>0.5 or x_range>0.5:
            x = random()*2-1
            range_weight = random()*2-1
            while x+range_weight>1 or x+range_weight<-1:
                range_weight = random()*2-1
            npi = randint(5,10)
        else:
            break
    #print(xy_mat);
    rotate_mat = [[np.cos(theta), -np.sin(theta)],[np.sin(theta), np.cos(theta)]]
    rotate_mat = np.array(rotate_mat)
    new_xy_mat = np.dot(rotate_mat, xy_mat)
    #print(new_xy_mat)
    temp = new_xy_mat*new_xy_mat;
    temp = temp[0, :]+temp[1, :]
    temp = 1-temp;
    new_z = -np.sqrt(temp)
    new_z = np.reshape(new_z, [1,LIGHT_NUMBER])
    lights = np.concatenate([new_xy_mat, new_z], axis = 0)
    lights = np.transpose(lights, [1,0])
    return lights

def output(lights):
    [row, col] = np.shape(lights)
    for i in range(row):
        print("%f, %f, %f"%(lights[i,0],lights[i,1], lights[i,2]))

def key_fun():
    theta = random()*2*np.pi
    x = random()*2-1 #[-1, 1]
    total_range = random()*2-1  # [-1, 1]
    while(x+total_range>1 or x+total_range<-1):
        total_range = random()*2-1
    #step = total_range/(LIGHT_NUMBER-1)
    npi = randint(5, 10)
    lights = gen_sin(x, total_range, npi, theta)
#    while lights.all()==None:
#        theta = random()*2*np.pi
#        x = random()*2-1 #[-1, 1]
#        total_range = random()*2-1  # [-1, 1]
#        while(x+total_range>1 or x+total_range<-1):
#            total_range = random()*2-1
#        npi = randint(10, 20)
#        lights = gen_sin(x, total_range, npi, theta)
    plt.plot(lights[:,0],lights[:,1])
    return lights
    
if __name__=="__main__":
    LIGHT_NUMBER = 5
    for i in range(100):
        
        lights = key_fun()
        
        output(lights)
        print()
