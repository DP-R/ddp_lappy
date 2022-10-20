import pygame
from pygame.locals import *
import sys
import numpy as np
import numpy.random as random
import math
import time
from additional_functions import *
from dataset_cm_cv_cr import positionmatrix,nr_experiments,nr_agents

data_matrix = np.zeros((nr_experiments*nr_agents, 4)) # Delete/comment after first run

j = 0 # add one after running

if j == nr_agents:
    print("nr of experiments reached")
    sys.exit()

pygame.init()
pygame.font.init() 
timefont = pygame.font.SysFont('Comic Sans MS', 30)
roomscreen = pygame.display.set_mode((800,800))
roomscreen.fill((255,255,255))
pygame.display.update()
clock = pygame.time.Clock()
background_color=(255,255,255)
class Agent(object):
    def __init__(self):
        
        self.mass = 80; self.radius = 20
        
        self.posx = random.uniform(100 + self.radius, 600 - self.radius)
        self.posy = random.uniform(100 + self.radius,700 - self.radius)
        self.avelx = 0
        self.avely = 0
        self.dest = np.array([random.uniform(100,700),random.uniform(100,700)])
    
        self.pos = np.array([self.posx, self.posy]);  self.avel = np.array([self.avelx, self.avely])
    
        self.direction = normalize(self.dest - self.pos)
        
        self.dSpeed = 12
        self.dvel = self.dSpeed*self.direction
        self.acclTime = 0.5
        self.bodyFactor = 120000
        self.F = 2000
        self.delta = 0.08*50 #random.uniform(0.8,1.6) #0.8 #0.08
        self.Goal = 0
        self.time = 0.0
        self.countcollision = 0
        print('X and Y Position:', self.pos);        print('self.direction:', self.direction)
        
    def velocity_force(self): 
        deltaV = self.dvel - self.avel
        return deltaV*self.mass/self.acclTime

    def f_ij(self, other): 
        r_ij = self.radius + other.radius
        d_ij = np.linalg.norm(self.pos - other.pos)
        e_ij = (self.pos - other.pos)/d_ij
        return self.F*np.exp((r_ij-d_ij)/(self.delta))*e_ij + self.bodyFactor*g(r_ij-d_ij)*e_ij

    def f_ik_wall(self, wall): 
        r_i = self.radius
        d_iw,e_iw = distance_agent_to_wall(self.pos,wall)
        return -self.F*np.exp((r_i-d_iw)/self.delta)*e_iw + self.bodyFactor*g(r_i-d_iw)*e_iw

    def update_dest(self):
        dist = math.sqrt((self.pos[0]-700)**2 + (self.pos[1]-400)**2)
        if dist < 300:
            self.dest = np.array([700,400])
        else:
            self.dest = np.array([700,400])
def main():
    agent_color = (0,255,0)
    line_color = (0,0,0)
    
    lb=[100,100];lt=[100,700]
    rb=[700,100];rt=[700,700]
    exit=[380,420]
    walls=[[lb[0],lb[1],rb[0],rb[1]  ],
           [lb[0],lb[1],lt[0],lt[1]  ],
           [lt[0],lt[1],rt[0],rt[1]  ],
           [rb[0],rb[1],rb[0],exit[0]],
           [rt[0],rt[1],rt[0],exit[1]]]
    
    agents = []
    for i in range(nr_agents):
        agent = Agent()
        agent.walls = walls
        agent.posx = positionmatrix[j*nr_agents+i][0]
        agent.posy = positionmatrix[j*nr_agents+i][1]
        agent.pos = np.array([agent.posx, agent.posy])
        agent.radius = positionmatrix[j*nr_agents+i][2]
        agent.mass = positionmatrix[j*nr_agents+i][3]
        agent.dSpeed = positionmatrix[j*nr_agents+i][4]
        agents.append(agent)
        
    count = 0
    start_time = time.time()
    run = True

    while run:
        if count < nr_agents - 2:
            current_time = time.time()
            elapsed_time = current_time - start_time
        else:
            for agent_i in agents:
                data_matrix[(j+1)*nr_agents - 2][0] = elapsed_time
                data_matrix[(j+1)*nr_agents - 1][0] = elapsed_time
                agents.remove(agent_i)
            for k in range(j*nr_agents, (j+1)*nr_agents):
                data_matrix[k][1] = elapsed_time
        
        dt = clock.tick(70)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = pygame.mouse.get_pos()
                print(x, y)
        
        roomscreen.fill(background_color)
        for wall in walls:
            pygame.draw.line(roomscreen, line_color,np.array([wall[0],wall[1]]) ,np.array([wall[2],wall[3]]) , 3)
        
        for agent_i in agents:
            agent_i.update_dest()
            agent_i.direction = normalize(agent_i.dest - agent_i.pos)
            agent_i.dvel = agent_i.dSpeed*agent_i.direction
            Velocity_force = agent_i.velocity_force()
            F_crowd = 0.0
            F_obstacle = 0.0
        
            for agent_j in agents: 
                if agent_i == agent_j: continue
                F_crowd += agent_i.f_ij(agent_j)
        
            for wall in walls:
                F_obstacle += agent_i.f_ik_wall(wall)
            
            agent_i.avel = agent_i.avel + (Velocity_force + F_crowd + F_obstacle)*dt/agent_i.mass 
            agent_i.pos = agent_i.pos + agent_i.avel*dt
            
            if agent_i.pos[0] > 750 or agent_i.pos[0] < 50 or agent_i.pos[1] > 750 or agent_i.pos[1] < 50:
                main()
                sys.exit()
        
        for agent_i in agents:
            
            agent_i.time += clock.get_time()/1000 
            start_position = [0, 0]
            start_position[0] = int(agent_i.pos[0])
            start_position[1] = int(agent_i.pos[1])
            
            end_position = [0, 0]
            end_position[0] = int(agent_i.pos[0] + agent_i.avel[0])
            end_position[1] = int(agent_i.pos[1] + agent_i.avel[1])
        
            end_positionDV = [0, 0]
            end_positionDV[0] = int(agent_i.pos[0] + agent_i.dvel[0])
            end_positionDV[1] = int(agent_i.pos[1] + agent_i.dvel[1])
        
            if start_position[0] >= 699 and agent_i.Goal == 0:
                agent_i.Goal = 1
                data_matrix[count+j*nr_agents][0] =  agent_i.time
            
            if start_position[0] > 699 or start_position[0] < 100:
                data_matrix[count+j*nr_agents][2] = count 
                data_matrix[count+j*nr_agents][3] = agent_i.countcollision 
                count += 1
                agents.remove(agent_i)
            
            pygame.draw.circle(roomscreen, agent_color, start_position, round(agent_i.radius), 3)
            pygame.draw.line(roomscreen, agent_color, start_position, end_positionDV, 2)
        pygame.draw.line(roomscreen, [255,60,0], start_position, end_positionDV, 2)
        timestr = "Time: " +  str(elapsed_time)
        timesurface = timefont.render(timestr, False, (0, 0, 0))
        roomscreen.blit(timesurface,(0,0))
        pygame.display.flip()
    pygame.quit()
main()
