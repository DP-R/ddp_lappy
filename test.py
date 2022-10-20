def cvtest():
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

def file_reader():
	
	# opening the file in read mode
	my_file = open("init_matrix_data.txt", "r")
	  
	# reading the file
	data = my_file.read()
	  
	# replacing end of line('/n') with ' ' and
	# splitting the text it further when '.' is seen.
	data_into_list = data.split("\n")
	pos=[]
	for i in data_into_list:
	    pos.append(i)
	    # print(i)
	# printing the data
	# print(data_into_list)
	my_file.close()

def scipysaver():
	import numpy as np
	import numpy.random as random
	a=np.random.uniform([10,10])
	print(a)
	import scipy.io as sio
	sio.savemat('a.mat',{'a':a})
	
def picklereader():
	from init_func import *
	from init_matrix import walls,nr_agents, nr_experiments
  
# from init_matrix import positionmatrix
	with open('init_matrix_data.pkl', 'rb') as file:    positionmatrix = pickle.load(file)

	a=np.array([[1,2,3],[2,3,4]])
	
def pygame_tester():
	import sys, pygame
	from pygame.locals import*

	width = 700
	height = 700
	screen_color = (49, 150, 100)
	line_color = (255, 0, 0)

	def mainer():
	    screen=pygame.display.set_mode((width,height))
	    screen.fill(screen_color)
    
	    pygame.draw.line(screen,line_color, (60, 80), (130, 100))
	    pygame.display.flip()
	    while True:
        	for events in pygame.event.get():
	            if events.type == QUIT or events.type==pygame.MOUSEBUTTONDOWN:
	                pygame.quit()
	mainer()


