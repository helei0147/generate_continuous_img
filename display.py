#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 15:38:03 2018

@author: urefrain
"""

import numpy as np
import random
import matplotlib.pyplot as plt
import gen_arc
import get_patch

block_buffer = np.load('results/blocks/1.npy')
light_buffer = np.load('results/lights/1.npy')
block_num = block_buffer.shape[0]//5
for i in range(20):
    index = random.randint(0,block_num-1)
    block = block_buffer[index*5:index*5+5,:,:]
    lights = light_buffer[index*5:index*5+5, :]
    block = np.transpose(block, [1,2,0])
    get_patch.save_block(block, 'temp/block_%d.png'%(i))
    gen_arc.display_lights(lights, 'temp/lights_%d.png'%(i))
    