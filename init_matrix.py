from init_func import *
import pickle

lt=[0,700];rt=[700,700];
lb=[0,100];rb=[700,100];
exit=[380,420]
walls=[[lb[0],lb[1],rb[0],rb[1]  ],
       [lb[0],lb[1],lt[0],lt[1]  ],
       [lt[0],lt[1],rt[0],rt[1]  ],
       [rb[0],rb[1],rb[0],exit[0]],
       [rt[0],rt[1],rt[0],exit[1]]]


random.seed(123)
nr_agents=100
nr_experiments=1

positionmatrix=[]
for j in range(0,nr_experiments):
 agents_found=0
 
 for i in range(0,nr_agents):
     found=False;countwall=0;
     
     while found==False:
         countwall=0; 
         desiredS=15; mass=80; radius=12/80*mass;dest=np.array([700,400])

         object_x=np.random.uniform(100,700);object_y=np.random.uniform(100,700);
         pos=np.array([object_x,object_y])

         for wall in walls:
             r_i=radius
             d_iw,e_iw=distance_agent_to_wall(pos,wall)
             
             if d_iw<r_i:
                 countwall+=1
         if len([positionmatrix[i] for i in range(j*nr_agents,j*nr_agents + agents_found)])>0:
             countagents=0
             for param in [positionmatrix[i] for i in range(j*nr_agents,j*nr_agents + agents_found)]:
                 dist=math.sqrt((param[0][0]-object_x)**2 + (param[0][1]-object_y)**2)
                 if dist>param[2]+radius:
                     countagents +=1
                 if countagents==i and countwall==0:
                     found=True; agents_found+=1;
         elif countwall==0:
             found=True; agents_found+=1;
         # found=True;agents_found+=1;
     positionmatrix.append([pos, mass, radius, desiredS, dest, j+1])

# np.savetxt('init_matrix_data',positionmatrix)
# for i in positionmatrix:
#     print(i)

# with open('init_matrix_data.txt', 'w') as f:
#     for i in positionmatrix:
#         f.write(f"{i}\n")

with open('init_matrix_data.pkl', 'wb') as file:
      
    # A new file will be created
    pickle.dump(positionmatrix, file)