# -*- coding: utf-8 -*-

from init_func import *
import pickle

box_size=15;
exit_size=1;
def wall1(box_size,exit_size):
    lt=[0,box_size];rt=[box_size,box_size];
    lb=[0,0];rb=[box_size,0];
    ex=[box_size/2-exit_size/2,box_size/2+exit_size/2]

    lt=[x*50+100 for x in lt]
    lb=[x*50+100 for x in lb]
    rt=[x*50+100 for x in rt]
    rb=[x*50+100 for x in rb]
    ex=[x*50+100 for x in ex]

    walls=[[lb[0],lb[1],rb[0],rb[1]  ],
           [lb[0],lb[1],lt[0],lt[1]  ],
           [lt[0],lt[1],rt[0],rt[1]  ],
           [rb[0],rb[1],rb[0],ex[0]  ],
           [rt[0],rt[1],rt[0],ex[1]  ]
           # ,
           # [rb[0],ex[0],rb[0],ex[1]  ]
           ]
    return walls

def wall2():
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

walls=wall1(box_size,exit_size)

random.seed(123)
nr_agents=100
nr_experiments=1

# positionmatrix=np.array([np.array([0,0]),0,0,0,np.array([]),0])
positionmatrix=np.empty(shape=[0,8],dtype=object)
for j in range(0,nr_experiments):
 agents_found=0
 
 for i in range(0,nr_agents):
     found=False;countwall=0;
     
     while found==False:
         countwall=0;
         (desiredS,mass,radius,dest)=(12,80,12,np.array([box_size,box_size/2])*50+100)

         # object_x=np.random.uniform(100,700);object_y=np.random.uniform(100,700);
         # pos=np.array([object_x,object_y])
         pos=np.array([np.random.uniform(0,box_size)+100,np.random.uniform(0,box_size)+100])
         for wall in walls:
             r_i=radius
             d_iw,e_iw=distance_agent_to_wall(pos,wall)
             
             if d_iw<r_i:
                 countwall+=1
         if len([positionmatrix[i] for i in range(j*nr_agents,j*nr_agents + agents_found)])>0:
             countagents=0
             for param in positionmatrix:
                 # print(param[0])
                 dist=math.sqrt((param[0]-pos[0])**2 + (param[1]-pos[1])**2)
                 if dist>param[3]+radius:
                     countagents +=1
                 if countagents==i and countwall==0:
                     found=True; agents_found+=1;
         elif countwall==0:
             found=True; agents_found+=1;
         # found=True;agents_found+=1;
     # positionmatrix.append(np.array([pos, mass, radius, desiredS, dest, j+1]))
     positionmatrix=np.vstack([positionmatrix,[pos[0],pos[1],mass,radius,desiredS,dest[0],dest[1],j+1]])
# for j in positionmatrix:
#     print(j)
# np.savetxt('init_matrix_data',positionmatrix)
# for i in positionmatrix:
    # print(i)

# with open('init_matrix_data.txt', 'w') as f:
#     for i in positionmatrix:
#         f.write(f"{i}\n")

with open('init_matrix_data.pkl', 'wb') as file:
      
    # A new file will be created
    pickle.dump(positionmatrix, file)

import scipy.io as sio
sio.savemat('positionmatrix.mat',{'positionmatrix':positionmatrix,'walls':walls,'nr_agents':nr_agents})

