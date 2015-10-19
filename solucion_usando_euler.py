#!/usr/bin/env python
# -*- coding: utf-8 -*-

from planeta import Planeta
import matplotlib.pyplot as plt
import numpy as np

#Main

condicion_inicial = [10.0, 0.0, 0.0, 0.15] #Vy inicial = 0.15

p = Planeta(condicion_inicial)

#Inicalización
t_final = 150.0 #spaceholder
dt = 0.1
N_pasos= t_final/dt

x = np.zeros(N_pasos)
y = np.zeros(N_pasos)
vx = np.zeros(N_pasos)
vy = np.zeros(N_pasos)

energia = np.zeros(N_pasos)