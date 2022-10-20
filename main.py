# package imports
import pygame
from pygame.locals import *
import sys
import numpy as np
import numpy.random as random
import math, time


# agent def
class Agent(object):
    # param init
    def __init__(self):

        # init chars
        self.mass=80
        self.radius=20

        # init params
        self.pos=np.array(random.uniform(lb[0]+self.radius,rb[0]-self.radius),random.uniform(lb[0]+self.radius,rb[0]-self.radius))
        self.vel=np.array([0,0])

        # final params
        self.pos_d=np.array([rt[0],rt[1]])
        self.direction=normalize(self.pos_d-self.pos)
        self.vel_d=1*self.direction

        # constant params
        self.acclTime=.5
        self.drivenAcc=(self.vel_d-self.vel)/self.acclTime
        self.bodyFactor=120000
        self.F=2000
        self.delta=.08*50

    # driving force
    def driving_force(self):
        dv=self.vel_d-self.vel
        return dv*self.mass/self.acclTime

    # collision force
    def F_ij(self,crowd):
        r_ij=self.radius+crowd.radius
        d_ij=np.linalg.norm(self.pos-crowd.pos)
        e_ij=(self.r-crowd.r)/d_ij
        return self.F*np.exp((r_ij-d_ij)/self.delta)*e_ij+self.bodyFactor*g(r_ij-d_ij)*e_ij

    # wall force
    def F_ik(self,wall):
        r_iw=self.radius
        d_iw=np.linalg.norm(self.)

    # param update
    def update_d(self):



    # define geometry
H_room=1000
W_room=1000

lb=[0,0];lt=[0,1000]
rb=[1000,0];rt=[1000,1000]

gate=[300,400]
walls=[lb[0],lb[1],rb[0],rb[1],
       lb[0],lb[1],lt[0],lt[1],
       lt[0],lt[1],rt[0],rt[1],
       rb[0],rb[1],rb[0],gate[0],
       rt[0],rt[1],rt[0],gate[1]]
    # display properties
pygame.init()
size = 800,800
disp= pygame.display.set_mode(size)
disp.fill((255,255,255))
pygame.display.update()

clock=pygame.time.Clock()
    # position matrix

    # display update

    # walls
for wall in walls:
    pygame.draw.line(disp, line_color, np.array([wall[0],wall[1]]),np.array([wall[2],wall[3]]))
    # agents
for agent in agents:
    agent.update_d()
    agent.direction=normalize(agent.pos_d-agent.pos)
    agent.vel_d=agent.driving_force()

    agent.vel=agent.vel+()
    agent.pos=agent.pos+agent.vel*dt
    # 