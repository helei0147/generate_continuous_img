import os,sys
import subprocess
import numpy as np
from scipy import misc
import random
import gen_arc

def read_patch(model_index, material_index):
    # read mask
    mask = misc.imread('mask/%d.png'% model_index)
    mask = mask>0
    transed_mask = np.transpose(mask, [1,0])
    [height, width] = mask.shape
    channels = np.zeros([height,width,3], dtype = np.float32)
    transed_channels = np.zeros([width, height,3], dtype = np.float32)
    gs_canvas = np.zeros([height, width], dtype = np.float32)
    folder_name = 'temp/%d_%d/' % (material_index, model_index)
    file_num = len(os.listdir(folder_name))
    patch_buffer = np.zeros([height, width, file_num])
    for i in range(file_num): # for each rgb file, read, please.
        filename = folder_name+str(i)+'.rgb'
        rgb = np.fromfile(filename, dtype = np.float32, count = -1);
        count_nan(rgb)
        transed_channels[transed_mask] = np.reshape(rgb,[-1,3])
        channels = np.transpose(transed_channels, [1,0,2])
        # new_value = 0.2989 * R + 0.5870 * G + 0.1140 * B
        gs_canvas = channels[:,:,0]*0.2989 + channels[:,:,1]*0.5870 + channels[:,:,2]*0.1140
        patch_buffer[:,:,i] = gs_canvas
    count_nan(patch_buffer)
    # save_block(patch_buffer, 'temp.png')
    # read patch pos
    a = np.load('pos_buffer/'+str(model_index)+'.npy')
    pos_num = a.shape[0]
    block_buffer = []
    info_buffer = []
    for i in range(pos_num):
        [top, bottom, left, right] = a[i]
        w = right-left; h = bottom-top; dep = patch_buffer.shape[2];
        cropped = patch_buffer[top:bottom, left:right, :]
        nonzero_pix_num = np.count_nonzero(cropped>0)
        valid_percent = np.sum(nonzero_pix_num)/(dep*w*h)
        if valid_percent>0.8:
            # save_block(cropped, str(i)+'.png')
            block_buffer.append(cropped)
            info_buffer.append([model_index, i])
    block_buffer = np.array(block_buffer)
    count_nan(block_buffer)
    info_buffer = np.array(info_buffer)
    print('block_buffer shape')
    print(block_buffer.shape)
    return block_buffer, info_buffer
def count_nan(matrix):
    nan_count = np.count_nonzero(np.isnan(matrix))
    if nan_count>0:
        print('nan occurs, nan count is %d'%(nan_count))
def save_block(blocks, pic_name):
    [h,w,d] = blocks.shape
    canvas = np.zeros([h, w*d], dtype = np.float32)
    for i in range(d):
        canvas[:,i*w:i*w+w] = blocks[:,:,i]
    med = np.median(canvas)
    if med>0:
        threshold = med*5
    else:
        threshold = 0.14
    print('threshold:', threshold)
    canvas[canvas>threshold] = threshold
    canvas = canvas/threshold*255
    canvas = canvas.astype(np.uint8)
    misc.imsave(pic_name, canvas)

if __name__ == '__main__':
    for file_index in range(4):
        block_buffer = []
        info_buffer = []
        mat_buffer = []
        light_buffer = []
        pos_buffer = []
        for i in range(1000):
            model_index = random.randint(0,9)
            material_index = random.randint(0,99)
            subprocess.call(r'python gen_arc.py', shell=True)
            #os.system(r'python gen_arc.py')
            lights = np.loadtxt('lights.txt')
            lights = np.reshape(lights, [-1, 3])
            # gen_arc.display_lights(lights)
            [light_num,_] = lights.shape;
            command = r'BRDF_Sphere.exe %d %d'%(model_index, material_index)
            subprocess.call(command, shell=True)
            #os.system(command)
            [block, info] = read_patch(model_index, material_index)
            block_num = block.shape[0]
            converted = np.transpose(block, [0,3,1,2])
            temp = np.concatenate(converted,axis=0)
            print(temp.shape)
            block_buffer.append(temp)
            for m in range(block_num):
                light_buffer.append(lights)
                for n in range(light_num):
                    mat_buffer.append(material_index)
                    info_buffer.append(info)
        block_buffer = np.array(block_buffer)
        block_buffer = np.concatenate(block_buffer, axis=0)
        light_buffer = np.array(light_buffer)
        light_buffer = np.concatenate(light_buffer, axis=0)
        mat_buffer = np.array(mat_buffer)
        info_buffer = np.array(info_buffer)
        print(block_buffer.shape)
        print(light_buffer.shape)
        print(mat_buffer.shape)
        print(info_buffer.shape)
        np.save('results/blocks/%d.npy'%(file_index), block_buffer)
        np.save('results/lights/%d.npy'%(file_index), light_buffer)
        np.save('results/mats/%d.npy'%(file_index), mat_buffer)
        np.save('results/info/%d.npy'%(file_index), info_buffer)
    