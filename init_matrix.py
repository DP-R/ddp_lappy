from init_func import *
import pickle

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
       [rb[0],rb[1],rb[0],ex[0]],
       [rt[0],rt[1],rt[0],ex[1]]]


random.seed(123)
nr_agents=10
nr_experiments=1

positionmatrix=np.array([np.array([0,0]),0,0,0,np.array([]),0])
positionmatrix=np.empty(shape=[0,6])
for j in range(0,nr_experiments):
 agents_found=0
 
 for i in range(0,nr_agents):
     found=False;countwall=0;
     
     while found==False:
         countwall=0;
         (desiredS,mass,radius,dest)=(4,70,0.3,np.array([700,400]))

         # object_x=np.random.uniform(100,700);object_y=np.random.uniform(100,700);
         # pos=np.array([object_x,object_y])
         pos=np.random.uniform([20,20])
         for wall in walls:
             r_i=radius
             d_iw,e_iw=distance_agent_to_wall(pos,wall)
             
             if d_iw<r_i:
                 countwall+=1
         if len([positionmatrix[i] for i in range(j*nr_agents,j*nr_agents + agents_found)])>0:
             countagents=0
             for param in [positionmatrix[i] for i in range(j*nr_agents,j*nr_agents + agents_found)]:
                 dist=math.sqrt((param[0][0]-pos[0])**2 + (param[0][1]-pos[1])**2)
                 if dist>param[2]+radius:
                     countagents +=1
                 if countagents==i and countwall==0:
                     found=True; agents_found+=1;
         elif countwall==0:
             found=True; agents_found+=1;
         # found=True;agents_found+=1;
     # positionmatrix.append(np.array([pos, mass, radius, desiredS, dest, j+1]))
     positionmatrix=np.vstack([positionmatrix,[pos,mass,radius,desiredS,dest,j+1]])
for j in positionmatrix:
    print(j)
# np.savetxt('init_matrix_data',positionmatrix)
# for i in positionmatrix:
#     print(i)

# with open('init_matrix_data.txt', 'w') as f:
#     for i in positionmatrix:
#         f.write(f"{i}\n")

with open('init_matrix_data.pkl', 'wb') as file:
      
    # A new file will be created
    pickle.dump(positionmatrix, file)

import scipy.io as sio
sio.savemat('positionmatrix.mat',{'positionmatrix':positionmatrix,'walls':walls,'nr_agents':nr_agents})