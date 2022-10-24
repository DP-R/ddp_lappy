def walltest():
    room_height = 600 # height of the room
    room_width = 600 # width of the room
    room_left = 100 # left pixels coordinate
    room_top = 100 # top pixels coordeinate

    door_xtop = room_left
    door_ytop = 382
    door_xbottom = room_left
    door_ybottom = 418

    walls = [[room_left, room_top, room_left + room_width, room_top], 
    [room_left, room_top, room_left, room_top + room_height],
    [room_left, room_top+room_height, room_left + room_width, room_top+ room_height],
    [660,375,660,425], [660,375,675,400], [675,400,660,425], # additional walls
    [room_left + room_width, room_top, room_left + room_width, door_ytop],
    [room_left+room_width, room_top + room_height, room_left + room_width, door_ybottom]]
 
    return walls
walltest()

def wall1():

    lt=[0,12];rt=[12,12];
    lb=[0,0];rb=[12,0];
    ex=[6-0.5,6+0.5]

    lt=[x*50+100 for x in lt]
    lb=[x*50+100 for x in lb]
    rt=[x*50+100 for x in rt]
    rb=[x*50+100 for x in rb]
    ex=[x*50+100 for x in ex]

    walls=[[lb[0],lb[1],rb[0],rb[1]  ],
           [lb[0],lb[1],lt[0],lt[1]  ],
           [lt[0],lt[1],rt[0],rt[1]  ],
           [rb[0],rb[1],rb[0],ex[0]  ],
           [rt[0],rt[1],rt[0],ex[1]  ]  ]
    return walls
a=wall1()
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
	
from init_func import *

def picklereader():
	from init_matrix import walls,nr_agents, nr_experiments
  
# from init_matrix import positionmatrix
	with open('init_matrix_data.pkl', 'rb') as file:    positionmatrix = pickle.load(file)

	a=np.array([[1,2,3],[2,3,4]])
	
from pygame.locals import*
def pygame_tester():
	import sys, pygame

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


