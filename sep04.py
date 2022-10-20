import pygame
from pygame.locals import *
import sys,os
import numpy as np
import numpy.random as random
import math
import time


lt=[100,700];rt=[700,700];
lb=[100,100];rb=[700,100];
exit=[380,420]
walls=[[lb[0],lb[1],rb[0],rb[1]  ],
       [lb[0],lb[1],lt[0],lt[1]  ],
       [lt[0],lt[1],rt[0],rt[1]  ],
       [rb[0],rb[1],rb[0],exit[0]],
       [rt[0],rt[1],rt[0],exit[1]]]

def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0:
       return v
    return v/norm

def g(x):    return np.max([x, 0])  

def distance_agent_to_wall(point, wall):
    p0 = np.array([wall[0],wall[1]])
    p1 = np.array([wall[2],wall[3]])
    d = p1-p0
    ymp0 = point-p0
    t = np.dot(d,ymp0)/np.dot(d,d)
    if t <= 0.0:
        dist = np.sqrt(np.dot(ymp0,ymp0))
        cross = p0 + t*d
    elif t >= 1.0:
        ymp1 = point-p1
        dist = np.sqrt(np.dot(ymp1,ymp1))
        cross = p0 + t*d
    else:
        cross = p0 + t*d
        dist = np.linalg.norm(cross-point)
    npw = normalize(cross-point)
    return dist,npw

random.seed(123)
nr_agents=100
nr_experiments=10
def init_random_pos():
    positionmatrix=[]
    for j in range(0,nr_experiments):
        agents_found=0
        
        for i in range(0,nr_agents):
            found=False;countwall=0;
            
            while found==False:
                countwall=0; 
                desiredS=20; mass=80; radius=12/80*mass;dest=np.array([700,400])

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
    return positionmatrix
class Agent(object):
    def __init__(self,pos,mass,radius,dSpeed,dest):
        self.pos=pos
        self.mass=mass
        self.radius=radius
        self.dSpeed=dSpeed
        self.dest=dest

        self.aVelocity=np.array([0,0])
        self.direction=normalize(self.dest-self.pos)
        self.dVelocity=self.dSpeed*self.direction

        self.acclTime=0.5
        self.bodyFactor=1200
        self.F=2000
        self.delta=4
    def velocity_force(self):
        return (self.dVelocity-self.aVelocity)*self.mass/self.acclTime
    def f_ij(self,other):
        r_ij = self.radius + other.radius
        d_ij = np.linalg.norm(self.pos-other.pos)
        e_ij = (self.pos-other.pos)/d_ij
        return self.F*np.exp((r_ij-d_ij)/(self.delta))*e_ij+self.bodyFactor*g(r_ij-d_ij)*e_ij
    def f_ik_wall(self,wall):
        r_i = self.radius
        d_iw,e_iw = distance_agent_to_wall(self.pos,wall)
        return -self.F*np.exp((r_i-d_iw)/self.delta)*e_iw+self.bodyFactor*g(r_i-d_iw)*e_iw

def agent_matrix():
    agents=[]
    for i in range(nr_agents):
        a=positionmatrix[i]
        agent=Agent(a[0],a[1],a[2],a[3],a[4])
        agents.append(agent)        
        # print(agent.direction,i)
    return agents

def draw_walls():
    for wall in walls:
        pygame.draw.line(roomscreen,line_color,([wall[0],wall[1]]),([wall[2],wall[3]]),3)
        pygame.display.flip()

def position_update():
    roomscreen.fill(background_color)
    dt=0.1
    for agent_i in agents:
        if agent_i.pos[0]>699 or agent_i.pos[0]<100:
            agents.remove(agent_i)

        aVelocity_force=agent_i.velocity_force()
        people_interaction=0;wall_interaction=0;

        for agent_j in agents:
            if agent_i == agent_j: continue
            people_interaction+=agent_i.f_ij(agent_j)
        for wall in walls:
            wall_interaction+=agent_i.f_ik_wall(wall)
        # print(aVelocity_force,people_interaction,wall_interaction)
        agent_i.aVelocity=agent_i.aVelocity+(aVelocity_force+people_interaction+wall_interaction)*dt/agent_i.mass
        agent_i.pos+=agent_i.aVelocity*dt

        pygame.draw.circle(roomscreen, agent_color, agent_i.pos, round(agent_i.radius), 3)
        pygame.draw.line(roomscreen, agent_color, agent_i.pos,agent_i.pos+10*agent_i.direction, 2)

WHITE = (255,255,255);RED = (255,0,0);GREEN = (0,255,0);BLACK = (0,0,0)
background_color = WHITE;agent_color = GREEN;line_color = BLACK

roomscreen = pygame.display.set_mode((800,800))
roomscreen.fill(background_color)
positionmatrix=init_random_pos()
agents=agent_matrix()
# pygame.display.update()

for i in range(100):
    # roomscreen.fill(background_color)
    draw_walls()
    position_update()

pygame.quit()
os.system('spd-say "done"')