'''
Used for extracting frames from given videos every nframes.
Usage:
    python imgs_from_videos.py --videosfolder xxx --savepath temp --n 1 --test
Created by Zhao Yinglong
'''
import os
import cv2
import glob
import argparse

fourcc=cv2.VideoWriter_fourcc('M','J','P','G')
writer=cv2.VideoWriter('output.mp4',fourcc,5,(640,512))

for i in range(9475,9658):
    frame=cv2.imread('..\data\val\thermal_8_bit')