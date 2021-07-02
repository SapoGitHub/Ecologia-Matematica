# -*- coding: UTF-8 -*-
"""
Autor: Jhordan Silveira de Borba (sbjhordan@gmail.com)
Site: https://sites.google.com/view/jdan/
"""

#Bibliotecas
import numpy as np                                      # Biblioteca de funções matemáticas
import copy                                             # Biblioteca com funções para copiar

#CONDIÇÕES INICIAIS ------------------------------------------------------
maxt = 15000    #tiempo total de cada realizacion
Lx   = 100      #tamaño del sustrato
Ly   = 100

#Fracciones iniciales
D    = 0.3  #fraccion inicial de sitios destruidos
x10  = 0.5  #fraccion inicial de sitios ocupados por x1
x20  = 0.5  #fraccion inicial de sitios ocupados por x2
y0   = 0.5  #fraccion inicial de sitios ocupados por y

#Tasas               
cx1   = 0.05   #colonizaciones       
cx2   = 0.1        
cy    = 0.015     
ex1   = 0.05   #extinciones       
ex2   = 0.01      
ey    = 0.017
mx1y  = 0.2    #depredaciones       
mx2y  = 0.8            
depx1 = ex1+mx1y       #mortalidad aumentada=extincion+depredacion
depx2 = ex2+mx2y


g = open("psd.dat", "r") 

#Inicializaciones
s  = np.full((Lx, Ly), [1])   #matriz de habitat (1=sitio disponible, 0=destruido)
x1 = np.full((Lx, Ly), [0])   #1 = sitio ocupado, 0 sitio vazio
x2 = np.full((Lx, Ly), [0])   #1 = sitio ocupado, 0 sitio vazio
y  = np.full((Lx, Ly), [0])   #1 = sitio ocupado, 0 sitio vazio

for i in range(1,Lx-1): 
  for j in range (1,Ly-1): 
    rnd=float(g.readline())#np.random.rand()
    if (rnd < D): s[i,j]=0
    rnd=float(g.readline())#np.random.rand()
    if (rnd < x10 and s[i,j]==1): x1[i,j]=1
    rnd=float(g.readline())#np.random.rand()
    if (rnd < x20 and s[i,j]==1): x2[i,j]=1
    rnd=float(g.readline())#np.random.rand()
    if ((x1[i,j]==1 or x2[i,j]==1) and rnd < y0): y[i,j]=1
    
for i in range(Lx): #destruimos los bordes del habitat
  s[i,0]=0
  s[i,Ly-1]=0
for j in range(Ly):
  s[0,j]=0
  s[Lx-1,j]=0

#-------------------------------------------------------
#Lazo temporal
fx1=sum(sum(x1))/((Lx-1)*(Ly-1)) #Original -1, acredito que deve ser -2
fx2=sum(sum(x2))/((Lx-1)*(Ly-1))
fy =sum(sum(y)) /((Lx-1)*(Ly-1))
f = open("minha.dat", "w")
f.write("	"+str(0)+"	"+str(fx1)+"	"+str(fx2)+"	"+str(fy)+"\n")

for it in range(maxt):
  if (float(it)%(float(maxt)/100)==0.):
    print("Porcentagem: "+str(it*100/maxt))  # Exibe o passo atual

  x1old=copy.copy(x1)              #poblaciones del paso anterior
  x2old=copy.copy(x2)
  yold=copy.copy(y)
  
  #Recorro la malla 
  for i in range (1,Lx-1):
    for j in range (1,Ly-1):
        
      #colonizaciones
      if (x1old[i,j]==0 and s[i,j]==1):                           #colonizacion de x1 si el sitio esta libre de x1 y no destruido:
        nvec=x1old[i-1,j]+x1old[i+1,j]+x1old[i,j-1]++x1old[i,j+1] #cantidad de vecinos ocupados
        p=1.0-(1.0-cx1)**nvec                                     #probabilidad de ser colonizado= 1 - prob de quedar libre
        rnd=float(g.readline())#np.random.rand() 
        if (rnd < p):x1[i,j]=1
      
      if (x2old[i,j]==0 and s[i,j]==1 and x1old[i,j]==0):         #colonizacion de x2 si el sitio esta libre de x1 y x2, y no destruido: 
        nvec=x2old[i-1,j]+x2old[i+1,j]+x2old[i,j-1]+x2old[i,j+1]  #cantidad de vecinos ocupados
        p=1.0-(1.0-cx2)**nvec                                     #probabilidad de ser colonizado= 1 - prob de quedar libre 
        rnd=float(g.readline())#np.random.rand()
        if (rnd < p): x2[i,j]=1                                

      ocup=0                                                       #ocupacion de herbivoros 
      if (x1old[i,j]==1 or x2old[i,j]==1): ocup=1
      if (yold[i,j]==0 and ocup==1):                               #colonizacion de y si el sitio está libre de y,y ocupado por un x 
        nvec=yold[i-1,j]+yold[i+1,j]+yold[i,j-1]+yold[i,j+1]       #cantidad de vecinos ocupados
        p=1.0-(1.0-cy)**nvec                                       #probabilidad de ser colonizado= 1 - prob de quedar libre 
        rnd=float(g.readline())#np.random.rand()
        if (rnd < p): y[i,j]=1

      #extinciones sin depredadores
      if (x1old[i,j]==1 and yold[i,j]==0):                          #extincion de x1 si el sitio esta ocupado 
        rnd=float(g.readline())#np.random.rand()
        if (rnd < ex1): x1[i,j]=0

      if (x2old[i,j]==1 and yold[i,j]==0):                          #extincion de x2 si el sitio esta ocupado 
        rnd=float(g.readline())#np.random.rand()
        if (rnd < ex2): x2[i,j]=0

      if (yold[i,j]==1):                                            #extincion de y si el sitio esta ocupado 
        rnd=float(g.readline())#np.random.rand()
        if (rnd < ey): y[i,j]=0

      #depredacion (extinción de presas donde hay depredadores)
      if (x1old[i,j]==1 and yold[i,j]==1):                          #depredacion de y sobre x1 
        rnd=float(g.readline())#np.random.rand()
        if (rnd < depx1): x1[i,j]=0

      if (x2old[i,j]==1 and yold[i,j]==1):                          #depredacion de y sobre x2 
        rnd=float(g.readline())#np.random.rand()
        if (rnd < depx2): x2[i,j]=0

      #desplazamiento por competencia (jerarquia)
      if (x1old[i,j]==1 and x2old[i,j]==1):
        rnd=float(g.readline())#np.random.rand()
        if (rnd < cx1): x2[i,j]=0
  
  fx1=sum(sum(x1))/((Lx-1)*(Ly-1))
  fx2=sum(sum(x2))/((Lx-1)*(Ly-1))
  fy =sum(sum(y)) /((Lx-1)*(Ly-1))
  f.write("	"+str(it+1)+"	"+str(fx1)+"	"+str(fx2)+"	"+str(fy)+"\n")
  
# CÁLCULOS FINAIS -----------------------------------------------------
f.close
g.close() 