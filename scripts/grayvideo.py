import numpy as np
import cv2

# 捕获视频
cap = cv2.VideoCapture('C:/Users/cmzyl/Documents/data/temp/20200410144550.avi')
# 定义编解码器，创建VideoWriter 对象
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output1.mp4',fourcc, 50.0, (384,288),False)
#（写出的文件，？？，帧率，（分辨率），是否彩色）  非彩色要把每一帧图像装换成灰度图
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        # frame = cv2.flip(frame,0)  #可以进行视频反转
        # write the flipped frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #换换成灰度图
        cv2.imwrite('saf.jpg',frame)
        out.write(frame)
        #cv2.imshow('frame',frame)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break
    else:
        break
# Release everything if job is finished
cap.release()
out.release()
#cv2.destroyAllWindows()