# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

def magnitude(vector):
    return math.sqrt(sum(pow(element, 2) for element in vector))
from init_func import *
from init_matrix import walls,nr_agents, nr_experiments
  
# from init_matrix import positionmatrix
with open('init_matrix_data.pkl', 'rb') as file:    positionmatrix = pickle.load(file)
pm=np.array(positionmatrix)
class Agent(object):
    def __init__(self,pos,mass,radius,dSpeed,dest):
        (self.pos,self.mass,self.radius,self.dSpeed,self.dest)=(pos,mass,radius,dSpeed,dest)

        self.aVelocity=np.array([0,0])
        self.direction=normalize(self.dest-self.pos)
        self.dVelocity=self.dSpeed*self.direction

        (self.acclTime,self.bodyFactor,self.F,self.delta)=(0.5,120000,2000,0.08*50)

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

r_i=pm[:,[2]]
d_i=pm[:,[0]]
ab=np.array([0,0])
(acclTime,bodyFactor,F,delta)=(0.5,120000,2000,0.08*50)
for j in range(len(r_i)):
    r_ij=r_i+r_i[j]
    d_ij=d_i-d_i[j]
    e_ij=np.divide(d_ij.T,np.array([magnitude(np.linalg.norm(x)) for x in d_ij]))
    d_ij=np.array([magnitude(np.linalg.norm(x)) for x in d_ij])
    d_ij=d_ij.reshape([nr_agents,1])
    ab=(F*np.exp((r_ij.astype(float)-d_ij)/(delta))*e_ij+bodyFactor*g(r_ij.astype(float)-d_ij)*e_ij)
    
    
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

def position_update(pos_mat,timer):
    # roomscreen.fill(background_color)
    dt=0.1
    for agent_i in agents:
        if agent_i.pos[0]>19.99:
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
        timer+=dt
        pos_mat.append([agent_i.pos,agent_i.mass,agent_i.radius,timer])
        # pygame.draw.circle(roomscreen, agent_color, agent_i.pos, round(agent_i.radius), 3)
        # pygame.draw.line(roomscreen, agent_color, agent_i.pos,agent_i.pos+10*agent_i.direction, 2)

WHITE = (255,255,255);RED = (255,0,0);GREEN = (0,255,0);BLACK = (0,0,0)
background_color = WHITE;agent_color = GREEN;line_color = BLACK

# roomscreen = pygame.display.set_mode((800,800))
# roomscreen.fill(background_color)
agents=agent_matrix()
pos_mat=[];timer=0;
# pygame.display.update()
a=time.time()
# while True:
for i in range(1):
    if len(agents)==1: 
        print(time.time()-a)
        break;
    # roomscreen.fill(background_color)
    # draw_walls()
    position_update(pos_mat,timer)
for i in pos_mat:
    print(i)
pygame.quit()
os.system('spd-say "done"')