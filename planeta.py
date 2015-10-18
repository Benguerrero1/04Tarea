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
        >> mercurio = Planeta([x0, y0, vx0, vy0])
        >> print(mercurio.alpha)
        >> 0.
        '''
        self.y_actual = condicion_inicial
        self.t_actual = 0.
        self.alpha = alpha

    def ecuacion_de_movimiento(self):
        '''
        Implementa la ecuación de movimiento, como sistema de ecuaciónes de
        primer orden.
        '''
        x, y, vx, vy = self.y_actual
        # fx = ...
        # fy = ...
        return [vx, vy, fx, fy]

    def avanza_euler(self, dt):
        '''
        Toma la condición actual del planeta y avanza su posicion y velocidad
        en un intervalo de tiempo dt usando el método de Euler explícito. El
        método no retorna nada, pero re-setea los valores de self.y_actual.
        '''
        x0, y0, vx0, vy0 = self.y_actual
        f=self.ecuacion_de_movimiento
        x1=x0+dt*f[0]
        y1=y0+dt*f[1]
        vx1=vx0+dt*f[2]
        vy1=vy0+dt*f[3]
        self.y_actual=[x1,y1,vx1,vy1]
        self.t_actual+=dt

    def avanza_rk4(self, dt):
        '''
        Similar a avanza_euler, pero usando Runge-Kutta 4.
        '''
        f = self.ecuacion_de_movimiento
        solver=ode(f)
        solver.set_integrator('dopri5', atol=1E-6, rtol=1E-4)
        solver.set_initial_value(self.y_actual)
        solver.integrate(self.t_actual+dt)
        self.y_actual=[solver.y[0],solver.y[1],solver.y[2],solver.y[3]]
        self.t_actual+=dt

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


