# -*- coding: utf-8 -*-

from init_func import *
from init_matrix import walls,nr_agents, nr_experiments
  
# from init_matrix import positionmatrix
with open('init_matrix_data.pkl', 'rb') as file:    positionmatrix = pickle.load(file)

    


a=np.array([[1,2,3],[2,3,4]])
