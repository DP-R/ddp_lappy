from init_func import *
from init_matrix import walls,nr_agents, nr_experiments
  
# from init_matrix import positionmatrix
with open('init_matrix_data.pkl', 'rb') as file:    positionmatrix = pickle.load(file)
for i in positionmatrix:
    print(i)
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
        self.bodyFactor=2000
        self.F=3000
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
    dt=0.05
    for agent_i in agents:
        if agent_i.pos[0]>699 or agent_i.pos[0]<100:
            agents.remove(agent_i)

        aVelocity_force=agent_i.velocity_force()
        print(aVelocity_force)
        people_interaction=0;wall_interaction=0;

        for agent_j in agents:
            if agent_i == agent_j: continue
            # print(agent_i.f_ij(agent_j))
            people_interaction+=agent_i.f_ij(agent_j)
        for wall in walls:
            wall_interaction+=agent_i.f_ik_wall(wall)
        # print(aVelocity_force,people_interaction,wall_interaction)
        agent_i.aVelocity=agent_i.aVelocity+(aVelocity_force+people_interaction+wall_interaction)*dt/agent_i.mass
        agent_i.pos+=agent_i.aVelocity*dt
        # print(agent_i.pos,agent_i.aVelocity)
        pygame.draw.circle(roomscreen, agent_color, agent_i.pos, round(agent_i.radius), 3)
        pygame.draw.line(roomscreen, agent_color, agent_i.pos,agent_i.pos+10*agent_i.direction, 2)

WHITE = (255,255,255);RED = (255,0,0);GREEN = (0,255,0);BLACK = (0,0,0)
background_color = WHITE;agent_color = GREEN;line_color = BLACK

roomscreen = pygame.display.set_mode((800,800))
# roomscreen.fill(background_color)
agents=agent_matrix()
# pygame.display.update()
from pygame_recorder import ScreenRecorder
recorder = ScreenRecorder(800, 800, 60)


for i in range(1):
    # roomscreen.fill(background_color)
    draw_walls()
    recorder.capture_frame(roomscreen)
    position_update()
    # print('done\n')
recorder.end_recording()
pygame.quit()
os.system('spd-say "done"')
