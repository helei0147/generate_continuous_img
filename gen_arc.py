# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 10:44:04 2018

@author: helei
"""
import curve
import numpy as np
import random
import matplotlib.pyplot as plt

from pylab import *
def gen_head_rear():
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
    return x1, y1, x2, y2
def gen_arc():
    LIGHT_NUMBER = 5
    while True:
        [x1, y1, x2, y2] = gen_head_rear()
        if x1*x1+x2*x2<1 and x2*x2+y2*y2<1:
            break
    
    x_range = x2-x1
    y_range = y2-y1
    delta_x = y_range
    delta_y = -x_range
    vertical_vec = np.array([delta_x,delta_y])
    while True:
        sign = 0
        if random()>0.5:
            sign = -1
        else:
            sign = 1
        weight = sign*(random()*1.5+0.5)
        head = np.array([x1,y1])
        rear = np.array([x2,y2])
        mid = (head+rear)/2
        circle_center = mid+weight*vertical_vec
        v1 = head-circle_center
        v2 = rear-circle_center
        vec_buffer = []
        for i in range(LIGHT_NUMBER):
            k = i/LIGHT_NUMBER
            v = v1*(1-k)+v2*k
            vec_buffer.append(v)
        point_buffer = []
        r1 = np.sqrt(np.sum(v1*v1))
        r2 = np.sqrt(np.sum(v2*v2))
        print('r1, r2: ', r1, r2)
        for vec in vec_buffer:
            vec_len = np.sqrt(np.sum(vec*vec))
            pos = circle_center+vec/vec_len*r1
            print('pos:', pos)
            point_buffer.append(pos)
        point_buffer = np.array(point_buffer)
        print('point_buffer shape: ', point_buffer.shape)
        x = point_buffer[:,0]
        y = point_buffer[:,1]
        if np.count_nonzero(1-x*x-y*y<0)>0:
            continue
        else:
            break
    z = -np.sqrt(1-x*x-y*y)
    x = np.reshape(x, [LIGHT_NUMBER, 1])
    y = np.reshape(y, [LIGHT_NUMBER, 1])
    z = np.reshape(z, [LIGHT_NUMBER, 1])
    lights = np.concatenate((x,y,z),axis=1)
    
    display_lights(lights)
    return lights
    
    
def gen_jumping_arc():
    LIGHT_NUMBER = 5
    [x1, y1, x2, y2] = gen_head_rear()
    x_range = x2-x1; x_length = np.abs(x_range);
    y_range = y2-y1; y_length = np.abs(y_range);
    
    steps = np.arange(LIGHT_NUMBER)
    x_step = x_range/(LIGHT_NUMBER-1)
    y_step = y_range/(LIGHT_NUMBER-1)
    x_steps = steps*x_step
    y_steps = steps*y_step
    x = x1+x_steps
    y = y1+y_steps
    
    eu_step = np.sqrt(x_step*x_step+y_step*y_step)
    k = y_range/x_range
    delta_x = y_step
    delta_y = -x_step
    
    for i in range(LIGHT_NUMBER-2):
        while True:
            weight = random()*2-1
            new_x = x[i+1]+weight*delta_x
            new_y = y[i+1]+weight*delta_y
            if(new_x*new_x+new_y*new_y<1):
                x[i+1] = new_x
                y[i+1] = new_y
                break
    
    z = -np.sqrt(1-x*x-y*y)
    x = np.reshape(x, [LIGHT_NUMBER, 1])
    y = np.reshape(y, [LIGHT_NUMBER, 1])
    z = np.reshape(z, [LIGHT_NUMBER, 1])
    lights = np.concatenate((x,y,z),axis=1)
    
    display_lights(lights)
    return lights
    
def output(file, lights):
    [light_num, dims] = lights.shape
    file.write('0 0 0 ')
    for i in range(light_num):
        file.write('%f %f %f '%(lights[i, 0], lights[i, 1], lights[i, 2]))
    file.close()
    
def display_lights(lights, filename = 'light_timg.png'):
    x = lights[:,0]
    y = lights[:,1]
    m = np.arange(-1,1,0.001)
    n1 = np.sqrt(1-m*m)
    n2 = -n1
    plt.figure(figsize=(6,6))
    plt.plot(-x,-y,m,n1,m,n2);
    plt.savefig(filename)
    
def gen_curve(Bezier_flag=True):
    
    while True:
        LIGHT_NUMBER = 5
        [x1, y1, x2, y2] = gen_head_rear()
        head = np.array([x1,y1])
        rear = np.array([x2,y2])
        center = (head+rear)/2
        r = curve.vec_len(rear-head)/np.sqrt(2)
        while True:
            theta = random()*2*np.pi
            anchor = np.array([r*np.sin(theta), r*np.cos(theta)])+center
            if curve.vec_len(anchor)<1:
                break
        if Bezier_flag:
            lights = curve.gen_Bezier(head, anchor, rear, LIGHT_NUMBER);
        else:
            lights = curve.gen_spiral(head, anchor, rear, LIGHT_NUMBER)
        if lights.shape[1]!=1:
            break
    return lights
        
    
if __name__ == "__main__":
    lights = gen_curve(False)
    #display_lights(lights)
    f = open('lights.txt','w')
    output(f, lights)
    f.close()