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

def img_extract(videopath,savepath,everyNseconds):
    capture=cv2.VideoCapture(videopath)
    if not capture.isOpened():
        print('Video %s open failed, please check the path'%videopath)
        exit()
    total_frames=capture.get(cv2.CAP_PROP_FRAME_COUNT)
    fps=capture.get(cv2.CAP_PROP_FPS)
    nframes=int(fps*everyNseconds)
    print('Total Frames: %d, FPS: %d'%(total_frames,fps))

    videoname=videopath.split('/')[-1]
    videoname=videoname.split('.')[0]
    imgpath=os.path.join(savepath,videoname)
    count=0
    while True:
        flag,frame=capture.read()
        if not flag:
            print('%s reading comleted'%videopath)
            break
        if count%nframes==0:
            cv2.imwrite(imgpath+'_'+str(count)+'.jpg',frame)
        count+=1
    
def main(args):
    videosfolder=args.videosfolder
    savepath=args.savepath
    nframes=args.n
    if not os.path.exists(videosfolder):
        print('%s does not exist!'%videosfolder)
        exit()
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    videos=glob.glob(videosfolder+'*.avi')
    if not videos:
        print('No videos found in given foloder %s'%videosfolder)
        exit()
    for video in videos:
        img_extract(video,savepath,nframes)
        if args.test:
            break

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Extract images from videos')
    parser.add_argument('--videosfolder',type=str,help='Path to videos folder')
    parser.add_argument('--savepath',default='temp',type=str,help='Path to save images')
    parser.add_argument('--n',default=1,type=int,help='extract one image from every n seconds')
    parser.add_argument('--test',action='store_true',default=False,help='if defined only run for single video')
    args=parser.parse_args()

    main(args)
