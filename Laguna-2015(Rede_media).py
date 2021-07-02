# -*- coding: UTF-8 -*-
"""
Autor: Jhordan Silveira de Borba (sbjhordan@gmail.com)
Site: https://sites.google.com/view/jdan/
"""

#Bibliotecas
import numpy as np                                      # Biblioteca de funções matemáticas
import copy                                             # Biblioteca com funções para copiar
import random

#CONDIÇÕES INICIAIS ------------------------------------------------------
maxt = 40000000    #tiempo total de cada realizacion
Lx   = 200      #tamaño del sustrato
Ly   = 200

#Fracciones iniciales
D    = 0.4  #fraccion inicial de sitios destruidos
x10  = 0.2  #fraccion inicial de sitios libres ocupados por x1
x20  = 0.2  #fraccion inicial de sitios libres ocupados por x2
y0   = 0.2  #fraccion inicial de sitios ocupdos por guanacos e ovelhas ocupados por y

#Tasas
M=4               
cx1   = M*0.05   #colonizaciones       
cx2   = M*0.1        
cy    = M*0.015     
ex1   = 0.05   #extinciones       
ex2   = 0.01      
ey    = 0.02
mx1y  = 0.2    #depredaciones       
mx2y  = 0.8            
depx1 = ex1+mx1y       #mortalidad aumentada=extincion+depredacion
depx2 = ex2+mx2y
con=0


#Inicializaciones
s  = np.full((Lx, Ly), [1])   #matriz de habitat (1=sitio disponible, 0=destruido)
x1 = np.full((Lx, Ly), [0])   #1 = sitio ocupado, 0 sitio vazio
x2 = np.full((Lx, Ly), [0])   #1 = sitio ocupado, 0 sitio vazio
y  = np.full((Lx, Ly), [0])   #1 = sitio ocupado, 0 sitio vazio

for i in range(1,Lx-1): 
  for j in range (1,Ly-1): 
    if (np.random.rand() < D): s[i,j]=0
    if (np.random.rand() < x10/(1-D) and s[i,j]==1): x1[i,j]=1
    if (np.random.rand() < x20/(1-D) and s[i,j]==1): x2[i,j]=1
    if (np.random.rand() <  y0/(1-D) and s[i,j]==1):  y[i,j]=1

for i in range(Lx): #destruimos los bordes del habitat
  s[i,0]=0
  s[i,Ly-1]=0
for j in range(Ly):
  s[0,j]=0
  s[Lx-1,j]=0

#-------------------------------------------------------
#Lazo temporal
fx1=sum(sum(x1))/((Lx-2)*(Ly-2)) #Original -1, acredito que deve ser -2
fx2=sum(sum(x2))/((Lx-2)*(Ly-2))
fy =sum(sum(y)) /((Lx-2)*(Ly-2))
f = open("minha.dat", "w")
f.write("	"+str(0)+"	"+str(fx1)+"	"+str(fx2)+"	"+str(fy)+"\n")

for it in range(maxt):
  if (float(it)%(float(maxt)/100)==0.):
    print("Porcentagem: "+str(it*100/maxt))  # Exibe o passo atual

  x1old=copy.copy(x1)              #poblaciones del paso anterior
  x2old=copy.copy(x2)
  yold=copy.copy(y)
       
  # COLONIZAÇÃO
  # Guanaco
  i=random.randint(1,Lx-1)
  j=random.randint(1,Ly-1)
  if (x1old[i,j]==1):
      i=random.randint(1,Lx-1)
      j=random.randint(1,Ly-1)
      if (s[i,j]==1 and x1old[i,j]==0):
          if (np.random.rand()<= cx1):
              x1[i,j]=1
              
  # Ovelha
  i=random.randint(1,Lx-1)
  j=random.randint(1,Ly-1)
  if (x2old[i,j]==1):
      i=random.randint(1,Lx-1)
      j=random.randint(1,Ly-1)
      if (s[i,j]==1 and (x1old[i,j]==0 and x2old[i,j]==0)):
          if (np.random.rand()<= cx2):
              x2[i,j]=1
              
  # Puma
  i=random.randint(1,Lx-1)
  j=random.randint(1,Ly-1)
  if (yold[i,j]==1):
      i=random.randint(1,Lx-1)
      j=random.randint(1,Ly-1)
      if (x1old[i,j]==1 or x2old[i,j]==1):
          if (np.random.rand()<= cy):
              y[i,j]=1
  
  #EXTINÇÃO LOCAL
  #Guanaco
  i=random.randint(1,Lx-1)
  j=random.randint(1,Ly-1)
  if (x1old[i,j]==1):
      if (np.random.rand()<= ex1):
              x1[i,j]=0
              
  #Ovelha
  i=random.randint(1,Lx-1)
  j=random.randint(1,Ly-1)
  if (x2old[i,j]==1):
      if (np.random.rand()<= ex2):
              x2[i,j]=0

  #Puma
  i=random.randint(1,Lx-1)
  j=random.randint(1,Ly-1)
  if (yold[i,j]==1):
      if (np.random.rand()<= ey):
              y[i,j]=0
      
   #PREDAÇÃO
   # Guanaco
  i=random.randint(1,Lx-1)
  j=random.randint(1,Ly-1)
  if (yold[i,j]==1):
      i=random.randint(1,Lx-1)
      j=random.randint(1,Ly-1)
      if ( x1old[i,j]==1):
          if (np.random.rand()<= mx1y):
              x1[i,j]=0
              
  # Ovelha
  i=random.randint(1,Lx-1)
  j=random.randint(1,Ly-1)
  if (yold[i,j]==1):
      i=random.randint(1,Lx-1)
      j=random.randint(1,Ly-1)
      if ( x2old[i,j]==1):
          if (np.random.rand()<= mx2y):
              x2[i,j]=0
              
   #deslocamento 
  i=random.randint(1,Lx-1)
  j=random.randint(1,Ly-1)
  if (x1old[i,j]==1):
      i=random.randint(1,Lx-1)
      j=random.randint(1,Ly-1)
      if ( x2old[i,j]==1):
          if (np.random.rand()<= cx1):
              x2[i,j]=0
                           
  if(con==20): #Salvar só a cada 10 passos
      fx1=sum(sum(x1))/((Lx-2)*(Ly-2))
      fx2=sum(sum(x2))/((Lx-2)*(Ly-2))
      fy =sum(sum(y)) /((Lx-2)*(Ly-2))
      f.write("	"+str(it+1)+"	"+str(fx1)+"	"+str(fx2)+"	"+str(fy)+"\n")
      con=0
  con=con+1
  
# CÁLCULOS FINAIS -----------------------------------------------------
f.close()