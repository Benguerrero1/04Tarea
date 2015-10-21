# -*- coding: utf-8 -*-



from planeta import Planeta
import matplotlib.pyplot as plt
import numpy as np

#Main

condicion_inicial = np.array([10.0, 0.0, 0.0, 0.25]) #Vy inicial = 0.25

p = Planeta(condicion_inicial)

#Inicalización
t_final = 900.0
dt = 0.1
N_pasos= int(t_final/dt)

x = np.zeros(N_pasos)
y = np.zeros(N_pasos)
vx = np.zeros(N_pasos)
vy = np.zeros(N_pasos)

E = np.zeros(N_pasos)

#Integración primer paso (rk4)
[x[0],y[0],vx[0],vy[0]] = condicion_inicial
E[0] = p.energia_total()
p.avanza_rk4(dt)
x1, y1, vx1, vy1 = p.y_actual
x[1] = x1
y[1] = y1
vx[1] = vx1
vy[1] = vy1
E[1] = p.energia_total()
#Integracion pasos restantes (Verlet)
for i in range(2,N_pasos):
    p.avanza_verlet(dt, x[i-2], y[i-2])
    xi, yi, vxi, vyi = p.y_actual
    x[i] = xi
    y[i] = yi
    vx[i] = vxi
    vy[i] = vyi
    E[i] = p.energia_total()

#Gráfico
fig=plt.figure(1,figsize=(8,6))
plt.subplot(2, 1, 1)
fig.subplots_adjust(hspace=.5)
plt.plot(x , y, label = "Trayectoria")
plt.title("Trayectoria bajo un potencial central, Verlet")
plt.xlabel("X")
plt.ylabel("Y")

t_values = np.linspace(1, t_final, N_pasos)
plt.subplot(2, 1, 2)
plt.plot(t_values, E)
plt.title("Energia en cada instante")
plt.xlabel("Tiempo")
plt.ylabel("Energia")

plt.savefig("Verlet.jpg")
plt.show()
