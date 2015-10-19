#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from scipy.integrate import ode
G=1
M=1
m=1
class Planeta(object):
    '''
    Complete el docstring.
    '''

    def __init__(self, condicion_inicial, alpha=0):
        '''
        __init__ es un método especial que se usa para inicializar las
        instancias de una clase.

        Ej. de uso:
        >> mercurio = Planeta(np.array([x0, y0, vx0, vy0])
        >> print(mercurio.alpha)
        >> 0.
        '''
        self.y_actual = condicion_inicial
        self.t_actual = 0.
        self.alpha = alpha

    def ecuacion_de_movimiento(self,datos=np.array([0,0,0,0])):
        '''
        Implementa la ecuación de movimiento, como sistema de ecuaciónes de
        primer orden. Recibe el array datos, que se suman a los valores de
        x, y, vx, y vy (esto hace rk4 más simple)
        Retorna un np.array por conveniencia.
        '''
        x, y, vx, vy = self.y_actual
        
        x += datos[0]
        y += datos[1]
        vx += datos[2]
        vy += datos[3]
        
        fx = x*G*M*((-1/np.sqrt(x**2+y**2)**3) + (2*self.alpha/(x**2+y**2)**2))
        fy = y*G*M*((-1/np.sqrt(x**2+y**2)**3) + (2*self.alpha/(x**2+y**2)**2))
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
        x0, y0, vx0, vy0 = self.y_actual
        vx, vy, fx, fy = self.ecuacion_de_movimiento
        Xn=2*x0-xp+dt**2*fx
        Yn=2*y0-yp+dt**2*fy
        Vxn=(Xn-xp)/2*dt
        Vyn=(Yn-yp)/2*dt
        self.y_actual=[Xn,Yn,Vxn,Vyn]
        self.t_actual+=dt

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


