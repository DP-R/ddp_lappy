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
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
background_color = WHITE
roomscreen.fill(background_color)
pygame.display.update()

agent_color = GREEN
line_color = BLACK

lt=[100,700];rt=[700,700];
lb=[100,100];rb=[700,100];
exit=[380,420]
walls=[[lb[0],lb[1],rb[0],rb[1]  ],
       [lb[0],lb[1],lt[0],lt[1]  ],
       [lt[0],lt[1],rt[0],rt[1]  ],
       [rb[0],rb[1],rb[0],exit[0]],
       [rt[0],rt[1],rt[0],exit[1]]]

clock = pygame.time.Clock()

class Agent(object):
    def __init__(self):
        
        self.mass = 80 
        self.radius = 20
        
        self.x = random.uniform(100 + self.radius, 700 - self.radius)
        self.y = random.uniform(100 + self.radius,700 - self.radius)
        self.pos = np.array([self.x, self.y])
    
        self.aVelocityX = 0 
        self.aVelocityY = 0  
        self.aVelocity = np.array([self.aVelocityX, self.aVelocityY])
    
        self.dest = np.array([random.uniform(100,700),random.uniform(100,700)])
        self.direction = normalize(self.dest - self.pos)
        
        self.dSpeed = 12
        self.dVelocity = self.dSpeed*self.direction
        
        self.acclTime = 0.5 
        self.drivenAcc = (self.dVelocity - self.aVelocity)/self.acclTime
              
        
        self.bodyFactor = 120000
        self.F = 2000
        self.delta = 0.08*50 
        
    def velocity_force(self): 
        deltaV = self.dVelocity - self.aVelocity
        if np.allclose(deltaV, np.zeros(2)):
            deltaV = np.zeros(2)
        return deltaV*self.mass/self.acclTime
    
    
    def f_ij(self, other): 
        r_ij = self.radius + other.radius
        d_ij = np.linalg.norm(self.pos - other.pos)
        e_ij = (self.pos - other.pos)/d_ij
        value = self.F*np.exp((r_ij-d_ij)/(self.delta))*e_ij
        + self.bodyFactor*g(r_ij-d_ij)*e_ij
        return value
    
    def f_ik_wall(self, wall): 
        r_i = self.radius
        d_iw,e_iw = distance_agent_to_wall(self.pos,wall)
        value = -self.F*np.exp((r_i-d_iw)/self.delta)*e_iw 
        + self.bodyFactor*g(r_i-d_iw)*e_iw
        return value
    
    def update_dest(self):
        dist = math.sqrt((self.pos[0]-700)**2 + (self.pos[1]-400)**2)
        if dist < 300:
            self.dest = np.array([700,400])
        else:
            self.dest = np.array([700,400])
 
def main():

    agents = []
    for i in range(nr_agents):
        agent = Agent()
        agent.posx = positionmatrix[j*nr_agents+i][0]
        agent.posy = positionmatrix[j*nr_agents+i][1]
        agent.pos = np.array([agent.posx, agent.posy])
        agent.radius = positionmatrix[j*nr_agents+i][2]
        agent.mass = positionmatrix[j*nr_agents+i][3]
        agent.dSpeed = positionmatrix[j*nr_agents+i][4]
        agents.append(agent)
     
    count = 0
    start_time = time.time()
    
    while True:
        # # Finding delta t for this frame
        dt = clock.tick(70)/1000
        roomscreen.fill(background_color)
        
        # draw walls
        for wall in walls:
            start_posw = np.array([wall[0],wall[1]])
            end_posw = np.array([wall[2],wall[3]])
            start_posx = start_posw 
            end_posx = end_posw
            pygame.draw.line(roomscreen, line_color, start_posx, end_posx, 3)
        
        for agent_i in agents:
            agent_i.update_dest()
            agent_i.direction = normalize(agent_i.dest - agent_i.pos)
            agent_i.dVelocity = agent_i.dSpeed*agent_i.direction
            aVelocity_force = agent_i.velocity_force()
            people_interaction = 0.0
            wall_interaction = 0.0
        
            for agent_j in agents: 
                if agent_i == agent_j: continue
                people_interaction += agent_i.f_ij(agent_j)
        
            for wall in walls:
                wall_interaction += agent_i.f_ik_wall(wall)
            
            sumForce = aVelocity_force + people_interaction + wall_interaction
            dv_dt = sumForce/agent_i.mass
            agent_i.aVelocity = agent_i.aVelocity + dv_dt*dt 
            agent_i.pos = agent_i.pos + agent_i.aVelocity*dt
            
            # Avoiding disappearing agents   
            if agent_i.pos[0] > 750 or agent_i.pos[0] < 50 or agent_i.pos[1] > 750 or agent_i.pos[1] < 50:
                main()
                sys.exit()
        
        for agent_i in agents:
            # agent_i.time += clock.get_time()/1000 
            start_position = [0, 0]
            start_position[0] = int(agent_i.pos[0])
            start_position[1] = int(agent_i.pos[1])
            
            end_position = [0, 0]
            end_position[0] = int(agent_i.pos[0] + agent_i.aVelocity[0])
            end_position[1] = int(agent_i.pos[1] + agent_i.aVelocity[1])
        
            end_positionDV = [0, 0]
            end_positionDV[0] = int(agent_i.pos[0] + agent_i.dVelocity[0])
            end_positionDV[1] = int(agent_i.pos[1] + agent_i.dVelocity[1])
        
            if start_position[0] > 699 or start_position[0] < 100:
                data_matrix[count+j*nr_agents][2] = count 
                agents.remove(agent_i)
            
            pygame.draw.circle(roomscreen, agent_color, start_position, round(agent_i.radius), 3)
            pygame.draw.line(roomscreen, agent_color, start_position, end_positionDV, 2)
        pygame.display.flip()
    pygame.quit()
main()
#np.savetxt('room1_vis', data_matrix)
