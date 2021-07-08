# -*- coding: UTF-8 -*-
"""
Simulação baseada no modelo de campo médio
Autor:           Jhordan Silveira de Borba
E-mail:          sbjhordan@gmail.com
Site:            https://sites.google.com/view/jdan/
Modelo original: Waves of desertification in a competitive ecosystem
Link:            https://fisica.cab.cnea.gov.ar/estadistica/abramson/papers/ecological/desertification.pdf
"""

#Bibliotecas
import numpy as np                                      # Biblioteca de funções matemáticas
import copy                                             # Biblioteca com funções para copiar
import random

#CONDIÇÕES INICIAIS ------------------------------------------------------
maxt = 500     #tiempo total de cada realizacion
Lx   = 100      #tamaño del sustrato en la coordenada x
Ly   = 100

#Fracciones iniciales
x10  = 0.3  #fraccion inicial de sitios ocupados por x1
x20  = 0.3  #fraccion inicial de sitios ocupados por x2
h0   = 1.  #fraccion inicial de sitios disponibles

#Tasas               
cx1   = 0.04         #colonizaciones       
cx2   = 0.7        
ex1   = 0.01         #extinciones       
ex2   = 0.01      
to    = 100        #Taxa de ocupação    #50
tr    = 20        #Taxa de recuperaçã  #20
g     = 0.1
t=tr+to

con1=1

#Inicializaciones
sh =[]   # Histórico damatriz de habitat
x2h=[]   # Histórico da matriz de voelhas
s  = np.full((Lx, Ly), [1])   # matriz de habitat (1=sitio disponible, 0=destruido)
x1 = np.full((Lx, Ly), [0])   # 1 = sitio ocupado, 0 sitio vazio
x2 = np.full((Lx, Ly), [0])   # 1 = sitio ocupado, 0 sitio vazio

sh.append(s)
x2h.append(x2)

# # Destruimos los bordes del habitat
# for i in range(Lx): 
#   s[i,0]=0
#   s[i,Ly-1]=0
# for j in range(Ly):
#   s[0,j]=0
#   s[Lx-1,j]=0
# Inicializamos a população inicial
for i in range(Lx): 
  for j in range (Ly):
    if (np.random.rand() < (1-h0) ): s[i,j]=0
    if (np.random.rand() < x10/h0 and s[i,j]==1): x1[i,j]=1
    if (np.random.rand() < x20/h0 and s[i,j]==1): x2[i,j]=1

#-------------------------------------------------------
#Lazo temporal
fx1=sum(sum(x1))/((Lx)*(Ly))
fx2=sum(sum(x2))/((Lx)*(Ly))
fs =sum(sum(s)) /((Lx)*(Ly))
f = open("temporal2019.dat", "w")
f.write("	"+str(0)+"	"+str(fx1)+"	"+str(fx2)+"	"+str(fs)+"\n")

for it in range(maxt):
    if (float(it)%(float(maxt)/100)==0.):
        print("Porcentagem: "+str(it*100/maxt))  # Exibe o passo atual
                
    sold =copy.copy(s )
    x1old=copy.copy(x1)              #poblaciones del paso anterior
    x2old=copy.copy(x2)
    
        
    for i in range (0,Lx-1):
        for j in range (0,Ly-1):
        #COLONIZAÇÃO+++++++++++++++++++++++++++++++++++
            #Guanaco
            if (x1old[i,j]==1):
                for a in range(1):
                    m=random.randint(0,Lx-1)
                    n=random.randint(0,Ly-1)
                    if (sold[m,n]==1 and x1old[m,n]==0):
                        if (np.random.rand()<= cx1):
                            x1[m,n]=1                
            #Ovelha
            if (x2old[i,j]==1):
                for a in range(1):
                    m=random.randint(0,Lx-1)
                    n=random.randint(0,Ly-1)
                    if (sold[m,n]==1 and (x1old[m,n]==0 and x2old[m,n]==0)):
                        if (np.random.rand()<= cx2):
                            x2[m,n]=1

            #EXTINÇÃO     
            #Guanaco
            if (x1old[i,j]==1):
                if (np.random.rand()<= ex1):
                        x1[i,j]=0
            #Ovelha
            if (x2old[i,j]==1):
                if (np.random.rand()<= ex2):
                        x2[i,j]=0
                        
            #DESLOCAMENTO+++++++++++++++++++++++++++++++++++++++++++++++++++
            if (x2old[i,j]==1):
                m=random.randint(0,Lx-1)
                n=random.randint(0,Ly-1)
                if ( x1old[m,n]==1):
                    if (np.random.rand()<= cx1):
                        x2[i,j]=0
                        
            #Dinâmica dos patches                      
            if(it+2>to):
                if (x2h[to-1][i,j]==1):
                    m=random.randint(0,Lx-1)
                    n=random.randint(0,Ly-1)
                    if (sh[to-1][m,n]==1):
                        if(np.random.rand()<=g):
                            li=np.where(s==1)  #Elementos que é 1
                            if(len(li[0])==1):
                                k=0
                            elif(len(li[0])>1):
                                k=random.randint(0,len(li[0])-1) #Sorteio do elemento
                                s[li[0][k],li[1][k]]=0
                           #     x1[li[0][k],li[1][k]]=0
                           #     x2[li[0][k],li[1][k]]=0
            if(it+2>t):      
                if (x2h[t-1][i,j]==1):
                    m=random.randint(0,Lx-1)
                    n=random.randint(0,Ly-1)
                    if (sh[t-1][m,n]==1):
                        if(np.random.rand()<=g):
                            li=np.where(s==0)  #Elementos que é 1
                            if (len(li[0])==1):
                                k=0
                            elif(len(li[0])>1):
                                k=random.randint(0,len(li[0])-1) #Sorteio do elemento
                                s[li[0][k],li[1][k]]=1                           
    sh.insert(0,copy.copy(s))
    x2h.insert(0,copy.copy(x2))
    if (it>=t):
        sh.pop()
        x2h.pop()

    if (con1==1):      
        fx1=sum(sum(x1))/((Lx)*(Ly))
        fx2=sum(sum(x2))/((Lx)*(Ly))
        fs =sum(sum(s ))/((Lx)*(Ly))
        f.write("	"+str(it+1)+"	"+str(fx1)+"	"+str(fx2)+"	"+str(fs)+"\n")
        if(fs>1):
            print("!")
        con1=0           
    con1=con1+1

# CÁLCULOS FINAIS -----------------------------------------------------
f.close()
