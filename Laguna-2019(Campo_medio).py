"""
Modelo baseado em um sistema de equações diferenciais com atraso
Autor:           Jhordan Silveira de Borba
E-mail:          sbjhordan@gmail.com
Site:            https://sites.google.com/view/jdan/
Modelo original: Waves of desertification in a competitive ecosystem
Link:            https://fisica.cab.cnea.gov.ar/estadistica/abramson/papers/ecological/desertification.pdf
"""
import matplotlib.pyplot as plt
import numpy as np


#Parâmetros da dinâmica
c1=0.04
c2=0.7
e1=0.01
e2=0.01
g=0.1
tr=10
to=50
t=tr+to

# Listas para guardar a evolução do sistema
x1=[]
x2=[]
h=[]

d=0.001 #Passo para o método de Euler

#Primeira parte:
N1=int(to/d)     #Quantidade de passos
x1.append(0.3)  #Condição inicial de guanacos
x2.append(0.3)  #Condição inicial de pumas
h.append(1.)     #Condição inicial de fragmentos disponíveis
    
#Resolve o sistema Usando o método de Euler
for k in range(N1):
    x1.append(x1[k]+d*(c1*(h[0]-x1[k]      )*x1[k]-e1*x1[k]))
    x2.append(x2[k]+d*(c2*(h[0]-x1[k]-x2[k]+x1[k]*x2[k])*x2[k]-e2*x2[k]-x1[k]*x2[k]*c1))
#    x2.append(x2[k]+d*(c2*(h[0]-x1[k]-x2[k]            )*x2[k]-e2*x2[k]               ))
    h.append(h[0])
    
#Segunda parte
N2=int(t/d)
for k in range(N1,N2):
    x1.append(x1[k]+d*(c1*(h[k]-x1[k]      )*x1[k]-e1*x1[k]))
    x2.append(x2[k]+d*(c2*(h[k]-x1[k]-x2[k]+x1[k]*x2[k])*x2[k]-e2*x2[k]-x1[k]*x2[k]*c1))
#    x2.append(x2[k]+d*(c2*(h[k]-x1[k]-x2[k]            )*x2[k]-e2*x2[k]               ))
    h.append(h[k]+d*(-g*x2[k-int(to/d)]*h[k-int(to/d)]))

#Terceira parte
N3=int(1000/d)
for k in range(N2,N3):
    x1.append(x1[k]+d*(c1*(h[k]-x1[k]      )*x1[k]-e1*x1[k]))
    x2.append(x2[k]+d*(c2*(h[k]-x1[k]-x2[k]+x1[k]*x2[k])*x2[k]-e2*x2[k]-x1[k]*x2[k]*c1))
#    x2.append(x2[k]+d*(c2*(h[k]-x1[k]-x2[k]            )*x2[k]-e2*x2[k]               ))
    h.append(h[k]+d*(-g*x2[k-int(to/d)]*h[k-int(to/d)]+g*x2[k-int(t/d)]*h[k-int(t/d)]))
    
#Plotar a evolução inteira
X=np.arange(len(x1)) #Eixo x
plt.plot(X,x1,'k-')
plt.plot(X,x2,'b-')
plt.plot(X,h,'g-')
plt.xlabel('Passo')
plt.ylim(0,1.1)
plt.show()

#sistema()
#Plotar a evolução inteira
# X=np.arange(int(2*t/d)) #Eixo x
# plt.plot(X,x2[len(x2)-int(2*t/d):],'k-')
# plt.plot(X,x1[len(x2)-int(2*t/d):],'b-')
# plt.plot(X, h[len(x2)-int(2*t/d):],'g-')
# plt.xlabel('Passo')
# plt.ylim(0,1)
# plt.show()

# print(abs(e1/c1-e2/c2-x2[N3-1]))
# print(abs(h[N3-1]-e1/c1-x1[N3-1]))

#sistema()