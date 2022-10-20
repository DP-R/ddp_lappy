with open('init_matrix_data.pkl', 'rb') as file:    positionmatrix = pickle.load(file)
pm=np.array(positionmatrix)

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
