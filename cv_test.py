import numpy as np
import cv2
img=np.zeros([800,800,3], dtype=np.uint8)
img.fill(255)
cv2.imwrite("a.png",img)
iml=[]
# height,width,layers=img[0].shape
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video=cv2.VideoWriter('video.avi',fourcc,1,(800,800))
for i in range(10):
    img=cv2.circle(img,(100+10*i,100),20,(255,60,0),3)
    iml.append(img)
    cv2.imshow("img",img)
    video.write(iml[i])
    cv2.waitKey(0)
# for i in range(10):
    # cv2.imshow
video.release()