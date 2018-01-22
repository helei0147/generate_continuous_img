# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 10:44:04 2018

@author: helei
"""
import numpy as np
import random
import matplotlib.pyplot as plt

from pylab import *

def gen_arc():
    LIGHT_NUMBER = 5
    x2 = x1 = 2
    y2 = y1 = 2
    while True:
        while True:
            x = random()*2-1
            y = random()*2-1
            if x*x+y*y<1:
                break
        x1 = x;y1 = y;
        while True:
            x = random()*2-1
            y = random()*2-1
            if x*x+y*y<1:
                break
        x2 = x; y2 = y;
        x_range = x2-x1; x_length = np.abs(x_range);
        y_range = y2-y1; y_length = np.abs(y_range);
        if x_length<0.5 and y_length<0.5 and x_length>0.2 and y_length>0.2:
            break
    
    steps = np.arange(LIGHT_NUMBER)
    x_steps = steps*x_range/(LIGHT_NUMBER-1)
    y_steps = steps*y_range/(LIGHT_NUMBER-1)
    x = x1+x_steps
    y = y1+y_steps
    m = np.arange(-1,1,0.001)
    n1 = np.sqrt(1-m*m)
    n2 = -n1
    plt.plot(x,y,m,n1,m,n2);
    z = -np.sqrt(1-x*x-y*y)
    x = np.reshape(x, [LIGHT_NUMBER, 1])
    y = np.reshape(y, [LIGHT_NUMBER, 1])
    z = np.reshape(z, [LIGHT_NUMBER, 1])
    lights = np.concatenate((x,y,z),axis=1)
    return lights
    
def output(file, lights):
    [light_num, dims] = lights.shape
    for i in range(light_num):
        file.write('%f %f %f '%(lights[i, 0], lights[i, 1], lights[i, 2]))
    file.close()
    
if __name__ == "__main__":
    lights = gen_arc()
    f = open('lights.txt','w')
    output(f, lights)