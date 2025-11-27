import cv2
import numpy as np
import os

tmp = os.listdir('./data/data2/source_images')
for i in range(10000):

    if tmp !=  os.listdir('./data/data2/source_images'):
        raise 'ERROR'
print(tmp)

