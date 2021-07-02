# -*- coding: UTF-8 -*-
"""
Autor: Jhordan Silveira de Borba (sbjhordan@gmail.com)
Site: https://sites.google.com/view/jdan/
"""

#Bibliotecas
import numpy as np                                      # Biblioteca de funções matemáticas
import copy                                             # Biblioteca com funções para copiar

#CONDIÇÕES INICIAIS ------------------------------------------------------
maxt = 6000     #tiempo total de cada realizacion
Lx   = 100      #tamaño del sustrato en la coordenada x
Ly   = 100

#Fracciones iniciales
x10  = 0.6  #fraccion inicial de sitios ocupados por x1
x20  = 0.5  #fraccion inicial de sitios ocupados por x2

#Tasas               
cx1   = 0.05         #colonizaciones       
cx2   = 0.7        
ex1   = 0.05         #extinciones       
ex2   = 0.01      
to    = 50         #Taxa de ocupação
tr    = 50         #Taxa de recuperaçã

#Inicializaciones
c =  np.full((Lx, Ly), [0])   # Relógio interno
s  = np.full((Lx, Ly), [1])   # matriz de habitat (1=sitio disponible, 0=destruido)
x1 = np.full((Lx, Ly), [0])   # 1 = sitio ocupado, 0 sitio vazio
x2 = np.full((Lx, Ly), [0])   # 1 = sitio ocupado, 0 sitio vazio


for i in range(Lx): #destruimos los bordes del habitat
  s[i,0]=0
  s[i,Ly-1]=0
for j in range(Ly):
  s[0,j]=0
  s[Lx-1,j]=0

for i in range(1,Lx-1): 
  for j in range (1,Ly-1): 
    rnd=np.random.rand()
    if (rnd < x10 and s[i,j]==1): x1[i,j]=1
    rnd=np.random.rand()
    if (rnd < x20 and s[i,j]==1): x2[i,j]=1

#-------------------------------------------------------
#Lazo temporal
fx1=sum(sum(x1))/((Lx-2)*(Ly-2))
fx2=sum(sum(x2))/((Lx-2)*(Ly-2))
fs =sum(sum(s)) /((Lx-2)*(Ly-2))
f = open("temporal2019.dat", "w")
f.write("	"+str(0)+"	"+str(fx1)+"	"+str(fx2)+"	"+str(fs)+"\n")

for it in range(maxt):
  if (float(it)%(float(maxt)/100)==0.):
    print("Porcentagem: "+str(it*100/maxt))  # Exibe o passo atual
    
  sold=copy.copy(s)
  x1old=copy.copy(x1)              #poblaciones del paso anterior
  x2old=copy.copy(x2)
  
  #Recorro la malla 
  for i in range (1,Lx-1):
    for j in range (1,Ly-1):
        
      #colonizaciones
      if (x1old[i,j]==0 and s[i,j]==1):                           #colonizacion de x1 si el sitio esta libre de x1 y no destruido:
        nvec=x1old[i-1,j]+x1old[i+1,j]+x1old[i,j-1]++x1old[i,j+1] #cantidad de vecinos ocupados
        p=1.0-(1.0-cx1)**nvec                                     #probabilidad de ser colonizado= 1 - prob de quedar libre
        rnd=np.random.rand() 
        if (rnd < p):x1[i,j]=1
      
      if (x2old[i,j]==0 and s[i,j]==1 and x1old[i,j]==0):         #colonizacion de x2 si el sitio esta libre de x1 y x2, y no destruido: 
        nvec=x2old[i-1,j]+x2old[i+1,j]+x2old[i,j-1]+x2old[i,j+1]  #cantidad de vecinos ocupados
        p=1.0-(1.0-cx2)**nvec                                     #probabilidad de ser colonizado= 1 - prob de quedar libre 
        rnd=np.random.rand()
        if (rnd < p): x2[i,j]=1                                

      #extinciones
      if (x1old[i,j]==1):                          #extincion de x1 si el sitio esta ocupado 
        rnd=np.random.rand()
        if (rnd < ex1): x1[i,j]=0

      if (x2old[i,j]==1):                          #extincion de x2 si el sitio esta ocupado 
        rnd=np.random.rand()
        if (rnd < ex2): 
            x2[i,j]=0
            c[i,j]=0 

      #desplazamiento por competencia (jerarquia)
      if (x1old[i,j]==1 and x2old[i,j]==1):
        rnd=np.random.rand()
        if (rnd < cx1): 
            x2[i,j]=0
            c[i,j]=0
            
      #Atualização dos relógios internos
      if (x2old[i,j]==1):
          c[i,j]=c[i,j]+1
          if (c[i,j]==to):
              c[i,j]=0
              s[i,j]=0
              x1[i,j]=0
              x2[i,j]=0
      elif (sold[i,j]==0):
          c[i,j]=c[i,j]+1
          if (c[i,j]==tr):
              c[i,j]=0
              s[i,j]=1
  
  fx1=sum(sum(x1))/((Lx-2)*(Ly-2))
  fx2=sum(sum(x2))/((Lx-2)*(Ly-2))
  fs =sum(sum(s)) /((Lx-2)*(Ly-2))
  f.write("	"+str(it+1)+"	"+str(fx1)+"	"+str(fx2)+"	"+str(fs)+"\n")
  
# CÁLCULOS FINAIS -----------------------------------------------------
f.close
