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

E = np.zeros(N_pasos)

#Integración
[x[0],y[0],vx[0],vy[0]] = condicion_inicial
E[0] = p.energia_total()
for i in range(1,N_pasos):
    p.avanza_euler(dt)
    xi, yi, vxi, vyi = p.y_actual
    x[i] = xi
    y[i] = yi
    vx[i] = vxi
    vy[i] = vyi
    E[i] = p.energia_total()

