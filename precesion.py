# -*- coding: utf-8 -*-



from planeta import Planeta
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

def es_afelio(r, valor, tolerancia):
    '''Recibe un valor de r, ve si está en el rango de tolerancia '''
    return (valor-tolerancia<r and r<valor+tolerancia)

#Main

condicion_inicial = np.array([10.0, 0.0, 0.0, 0.25]) #Vy inicial = 0.25

p = Planeta(condicion_inicial, 10**(-2.370))

#Inicalización
t_final = 5400.0
dt = 0.1
N_pasos= int(t_final/dt)

x = np.zeros(N_pasos)
y = np.zeros(N_pasos)
vx = np.zeros(N_pasos)
vy = np.zeros(N_pasos)
r = np.zeros(N_pasos)

E = np.zeros(N_pasos)
afelio = [[], [], []]

#Integración primer paso (rk4)
[x[0],y[0],vx[0],vy[0]] = condicion_inicial
r[0]=np.sqrt(x[0]**2+y[0]**2)
E[0] = p.energia_total()
p.avanza_rk4(dt)
x1, y1, vx1, vy1 = p.y_actual
x[1] = x1
y[1] = y1
vx[1] = vx1
vy[1] = vy1
E[1] = p.energia_total()
r[1]=np.sqrt(x[1]**2+y[1]**2)
#Integracion pasos restantes (Verlet) y comprobación si es afelio o no
for i in range(2,N_pasos):
    p.avanza_verlet(dt, x[i-2], y[i-2])
    xi, yi, vxi, vyi = p.y_actual
    x[i] = xi
    y[i] = yi
    vx[i] = vxi
    vy[i] = vyi
    r[i]=np.sqrt(x[i]**2+y[i]**2)
    E[i] = p.energia_total()
    
    tolerancia = 0.000005
    valor_estimado =10

    if es_afelio(r[i],valor_estimado, tolerancia):
        afelio[0].append(p.t_actual)
        afelio[1].append(x[i])
        afelio[2].append(y[i])
        
#Cálculo velocidades angulares
        
vel_angular = np.zeros(len(afelio[0])-1)

phi_anterior =  np.arctan(afelio[2][0]/(afelio[1][0]))
t_anterior = afelio[0][0]
for i in range(1,len(afelio[0])):
    phi = np.arctan(afelio[2][i]/(afelio[1][i]))
    t = afelio[0][i]
    dphi = phi - phi_anterior
    dt = t-t_anterior

    vel_angular[i-1] = dphi/dt

    t_anterior = t
    phi_anterior = phi
vel_angulares = np.round(vel_angular,7)

velocidad_precesion = scipy.stats.tmean(vel_angulares)
print("velocidad angular de precesion = "+(str)(vel_angulares))
print("velocidad angular de precesion = "+(str)(velocidad_precesion))

#Gráfico
fig=plt.figure(1,figsize=(8,6))
plt.subplot(2, 1, 1)
fig.subplots_adjust(hspace=.5)
plt.plot(x , y, label = "Trayectoria")
plt.title("Integracion Verlet para $\\alpha = 10^{-2.370}$")
plt.xlabel("X")
plt.ylabel("Y")

t_values = np.linspace(1, t_final, N_pasos)
plt.subplot(2, 1, 2)
plt.plot(t_values, E)
plt.title("Energia en cada instante")
plt.xlabel("Tiempo")
plt.ylabel("Energia")

plt.savefig("PrecesionVerlet.jpg")
plt.show()
