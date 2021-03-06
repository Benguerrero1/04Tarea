#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from scipy.integrate import ode
G=1
M=1
m=1
class Planeta(object):
    '''
    Define un planeta que orbita alrededor del Sol en una orbita cercana,
    por lo que cumple la ecuacion modificada de la energia potencal gravitatoria.
    '''

    def __init__(self, condicion_inicial, alpha=0):
        self.y_actual = condicion_inicial
        self.t_actual = 0.
        self.alpha = alpha

    def ecuacion_de_movimiento(self,datos=np.array([0,0,0,0])):
        '''
        Implementa la ecuacion de movimiento, como sistema de ecuaciones de
        primer orden. Recibe el array datos, que se suman a los valores de
        x, y, vx, y vy (esto hace rk4 más simple)
        Retorna un np.array por conveniencia.
        '''
        x, y, vx, vy = self.y_actual
        
        x += datos[0]
        y += datos[1]
        vx += datos[2]
        vy += datos[3]
        r=np.sqrt(x**2+y**2)
        
        fx = x*G*M*((-1/r**3) + (2*self.alpha/r**4))
        fy = y*G*M*((-1/r**3) + (2*self.alpha/r**4))
        return np.array([vx, vy, fx, fy])

    def avanza_euler(self, dt):
        '''
        Toma la condición actual del planeta y avanza su posicion y velocidad
        en un intervalo de tiempo dt usando el método de Euler explícito. El
        método no retorna nada, pero re-setea los valores de self.y_actual.
        '''
        yn = self.y_actual + dt * (self.ecuacion_de_movimiento())
        self.y_actual = yn
        self.t_actual += dt
        pass

    def avanza_rk4(self, dt):
        '''
        Similar a avanza_euler, pero usando Runge-Kutta 4.
        '''
        k1 = self.ecuacion_de_movimiento()
        k2 = self.ecuacion_de_movimiento(dt/2. * k1)
        k3 = self.ecuacion_de_movimiento(dt/2. * k2)
        k4 = self.ecuacion_de_movimiento(dt * k3)

        yn = self.y_actual + dt/6. * (k1 + 2*k2 + 2*k3 + k4)

        self.y_actual = yn
        self.t_actual += dt
        pass
        

    def avanza_verlet(self, dt, xp, yp):
        '''
        Similar a avanza_euler, pero usando Verlet.
        xp e yp son las posiciones previas.
        '''
        P_previa = np.array([xp, yp])
        x0, y0, vx0, vy0 = self.y_actual
        P_actual = np.array([x0, y0])
        Pn = 2 * P_actual - P_previa + dt**2 * self.ecuacion_de_movimiento()[2:]
        Vn=(Pn - P_previa) / 2 * dt
        self.y_actual = np.array([Pn[0], Pn[1], Vn[0], Vn[1]])
        self.t_actual += dt
        pass

    def energia_total(self):
        '''
        Calcula la energía total del sistema en las condiciones actuales.
        '''
        x, y, vx, vy = self.y_actual
        r=np.sqrt(x**2+y**2)
        potencial=G*M*m*(-1/r+self.alpha*1/r**2)
        cinetica=(vx**2+vy**2)*m/2
        energia=potencial+cinetica
        return (energia)


