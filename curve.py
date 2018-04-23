# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 16:55:18 2018

@author: helei
"""

import numpy as np
import matplotlib.pyplot as plt

def dis_lights(lights, filename = 'light_timg.png'):
    x = lights[:,0]
    y = lights[:,1]
    m = np.arange(-1,1,0.001)
    n1 = np.sqrt(1-m*m)
    n2 = -n1
    plt.figure(figsize=(6,6))
    plt.plot(-x,-y,m,n1,m,n2);
    plt.savefig(filename)

def from_2_to_3(insert_buffer):
    x = insert_buffer[:, 0]
    y = insert_buffer[:, 1]
    z = -np.sqrt(1-x*x-y*y)
    x = np.reshape(x, [-1, 1])
    y = np.reshape(y, [-1, 1])
    z = np.reshape(z, [-1, 1])
    lights = np.concatenate([x,y,z], 1)
    return lights

def gen_Bezier(head, anchor, rear, density):
    percent = np.arange(density)/float(density-1)
    insert_buffer = []
    for k in percent:
        p1 = (1-k)*head+k*anchor
        p2 = (1-k)*anchor+k*rear
        p3 = (1-k)*p1+k*p2
        insert_buffer.append(p3)
    insert_buffer = np.array(insert_buffer)
    insert_buffer = from_2_to_3(insert_buffer)
    return insert_buffer

def vec_len(vec):
    return np.sqrt(np.sum(vec*vec))

def gen_spiral(head, center, rear, density):
    percent = np.arange(density)/float(density-1)
    insert_buffer = []
    len1 = vec_len(head-center)
    len2 = vec_len(rear-center)
    for k in percent:
        direction = ((1-k)*head+k*rear)-center
        d_len = vec_len(direction)
        direction = direction/d_len
        r = (1-k)*len1+k*len2
        p = r*direction+center
        insert_buffer.append(p)
    available = True
    for vec in insert_buffer:
        if vec_len(vec)>=1:
            available = False
    if available == False: # 如果给定的三个锚点不能够生成有效的光照， 返回一个大小为1x1的零矩阵
        return np.zeros([1,1])
    insert_buffer = np.array(insert_buffer)
    insert_buffer = from_2_to_3(insert_buffer)
    return insert_buffer
    
if __name__ == '__main__':
    p1 = np.array([-0.5,-0.5])
    p2 = np.array([0.5, 0.5])
    anchor = np.array([-1, 1])
    lights = gen_spiral(p1, p2, anchor, 5);
    print(lights.shape)
    dis_lights(lights)
    