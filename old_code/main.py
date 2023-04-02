from init_func import *
from init_matrix import walls,nr_agents, nr_experiments
  
# from init_matrix import positionmatrix
# with open('init_matrix_data.pkl', 'rb') as file:    positionmatrix = pickle.load(file)
# for i in positionmatrix:
    # print(i)


def draw_walls():
    for wall in walls:
        pygame.draw.line(roomscreen,line_color,([wall[0],wall[1]]),([wall[2],wall[3]]),3)
        pygame.display.flip()

def position_update(timestep):
    roomscreen.fill(background_color)
    # dt=0.05
    for i in range(nr_agents):
        j=i+timestep
        if finalmat[j,8]==1:
            pygame.draw.circle(roomscreen, agent_color, finalmat[j,[0,1]], round(finalmat[j,3]), 3)
            pygame.draw.line(roomscreen, agent_color, finalmat[j,[0,1]],finalmat[j,[0,1]]+1*finalmat[j,[4,5]], 2)

WHITE = (255,255,255);RED = (255,0,0);GREEN = (0,255,0);BLACK = (0,0,0)
background_color = WHITE;agent_color = GREEN;line_color = BLACK

# roomscreen.fill(background_color)
# agents=agent_matrix()
# pygame.display.update()

import scipy.io as sio
finalmat=sio.loadmat('finalmat.mat')
finalmat=finalmat['finalmat']
# for i in finalmat:
#     print(i)
roomscreen = pygame.display.set_mode((800,800))
from pygame_recorder import ScreenRecorder
recorder = ScreenRecorder(800, 800, 60)

def allpos():
    for timestep in range(finalmat.shape[0]//nr_agents):
        # roomscreen.fill(background_color)
        draw_walls()
        recorder.capture_frame(roomscreen)
        position_update(timestep*nr_agents)
        # print('done\n')
    recorder.end_recording()
    pygame.quit()
    os.system('spd-say "done"')

def onepos(i):
    for timestep in range(finalmat.shape[0]//nr_agents):
        roomscreen.fill(background_color)
        draw_walls()
        recorder.capture_frame(roomscreen)
        # position_update(timestep*nr_agents)
        # for i in range(nr_agents):
        j=i+timestep*nr_agents
        pygame.draw.circle(roomscreen, agent_color, finalmat[j,[0,1]], round(finalmat[j,3]), 3)
        pygame.draw.line(roomscreen, agent_color, finalmat[j,[0,1]],finalmat[j,[0,1]]+1*finalmat[j,[4,5]], 2)
            # print('done\n')
    recorder.end_recording()
    pygame.quit()
    os.system('spd-say "done"')
    # dt=0.05
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type== pygame.MOUSEBUTTONDOWN:
            pygame.quit()
            sys.exit()

allpos()
# onepos(1)
# print(finalmat[11,:])

 

# import cv2
# img=np.zeros([800,800,3],dtype=np.uint8)
# img.fill(255)
# for i in range(10):
    # img=cv2.circle(img,finalmat[i+10,[0,1]],20,(255,60,0),3)
    # cv2.waitkey(0)