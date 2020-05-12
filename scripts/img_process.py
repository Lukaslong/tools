import os
import glob
import cv2
import sys
import argparse

'''
default:
input:  1920*1080
crop:   from (360,180) to (1560,1080)
resize: from 1200*900 to 640*480
'''

def main(args):
    img_path=args.img_path
    save_path=args.save_path
    img_files=glob.glob(img_path+os.sep+'*.jpg')
    for img_name in img_files:
        image=cv2.imread(img_name)
        image_crop=image[90:990,360:1560,:]
        img_resize=cv2.resize(image_crop,(640,480))
        new_name=os.path.join(save_path,img_name.split('/')[-1])
        cv2.imwrite(new_name,img_resize)
        print(new_name,'has been saved')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Image processing')
    parser.add_argument('--img-path',help='Path to images flolder')
    parser.add_argument('--save-path',help='Path to save processed imgs')
    parser.add_argument('--crop-size',help='operation to images')

    args=parser.parse_args()

    main(args)
