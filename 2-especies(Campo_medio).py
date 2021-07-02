# -*- coding: utf-8 -*-
"""
Autor: Jhordan Silveira de Borba (sbjhordan@gmail.com)
Site: https://sites.google.com/view/jdan/
"""

import matplotlib.pyplot as plt
import numpy as np

# SOLUÇÕES LOTKA VOLTERRA

def phase_lot():
    p1=[0.,0.] # Ponto de equilíbrio 1
    p2=[0.65,0.] # Ponto de equilíbrio 1
    p3=[-3.26799426659511,1.305998088865036]
    p4=[0.9179942665951096,-0.08933142219836986]
    
    #PLANO DE FASE LOTKA-VOLTERRA
    X = np.arange(0,1, 0.1/2)
    Y = np.arange(0,1, 0.1/2)
    U,V=np.meshgrid(X,Y)
        
    c=0
    for x in X:
        l=0
        for y in Y:
            #Distâncias
            d=[]
            d.append(np.sqrt((x-p1[0])*(x-p1[0])+(y-p1[1])*(y-p1[1])))
            d.append(np.sqrt((x-p2[0])*(x-p2[0])+(y-p2[1])*(y-p2[1])))
            d.append(np.sqrt((x-p3[0])*(x-p3[0])+(y-p3[1])*(y-p3[1])))
            d.append(np.sqrt((x-p4[0])*(x-p4[0])+(y-p4[1])*(y-p4[1])))
            for i in range(len(d)):
                if (min(d)==d[i]):
                    p=i
            
           # p=3
            #Calculamos o vetor baseado no ponto mais próximo:
            if(p==0):
                u=x-p1[0]
                v=y-p1[1]
                a=(13*u)/200
                b=-(3*v)/200
                
            elif (p==1):
                u=x#-p2[0]
                v=y#-p2[1]
                a=-(702561541869797376*v+234187180623265792*u+25)/3602879701896396800
                b=-(21*v)/4000
    
            elif(p==2):
                u=x#-p3[0]
                v=y#-p3[1]                                       
                a=(2856462442699113328307435732992*v+952154147566371860035749806080*u-646943275529005)/2913573494602275041491529236480
                b=(1106961390787556*v-103650142073625*u)/17290891562367850
            elif(p==3):
                u=x#-p4[0]
                v=y#-p4[1]                                       
                a=-(476383484640770473543180327321600*v+158794494880256872552789467725824*u+12002887083222133)/1729798329451818809271355468414976
                b=(222890786286285095300881195929600*v-264491779584545541582020359839744*u-66304146739623397)/181199351989854269545634167733096448
            else:
                print("Algo deu errado")
            m=np.sqrt(a*a+b*b)
            if(m==0):
                m=1
            U[l,c]=a/m
            V[l,c]=b/m
            l=l+1
        c=c+1
    
    fig, ax = plt.subplots()
    ax.quiver(X, Y, U, V)
    plt.plot(p1[0],p1[1],'ro')
    plt.show()

def phase2():
    #Parâmetros
    
    M=4
    c1=M*0.1 #0.05#0.1      # Fator de colonização do guancamo 
    cy=M*0.015               # Fator de colonização do puma
    e1=0.025   #0.05#0.025    # Fator de extinção local do guancamo
    ey=0.015  #0.02#0.015    # Fator de extinção local do puma
    u1=0.3    #0.2#0.3       # Fator de predação do guancamo
    N=int(200000)#+300000)
    d=0.01
    D=0.5
    
    
    #p1=[0.,0.] # Ponto de equilíbrio 1
    #p2=[0.65,0.] # Ponto de equilíbrio 1
    #p3=[-3.26799426659511,1.305998088865036]
    #p=[0.9179942665951096,-0.08933142219836986]
    
    #Variáveis
    #Valores iniciais:
    #init=[(p[0]-0.1,p[1]-0.1),(p[0]+0.1,p[1]+0.1),(p[0]-0.1,p[1]+0.1),(p[0]+0.1,p[1]-0.1)]
    init=[(0.4,0.4),(0.3,0.3),(0.05,0.05)]
    c=0
    for it in init:
        x=[]
        y=[]
        x.append(it[0])
        y.append(it[1])
        for i in range(N-1):
            x.append(x[i]+d*(c1*x[i]*(1-D-x[i])-e1*x[i]-u1*x[i]*y[i]))
            y.append(y[i]+d*(cy*y[i]*(x[i]-y[i]*(x[i]))-ey*y[i]))
        if(c==0):
            plt.plot(x,y,'g-')
            plt.plot(it[0],it[1],'go')
            D=0.7
        elif (c==1):
            plt.plot(x,y,'b-')
            plt.plot(it[0],it[1],'bo')
            D=0.95
        else:
            plt.plot(x,y,'r-')
            plt.plot(it[0],it[1],'ro')
        c=c+1
        
    #plt.plot(p[0],p[1],'ro')
    #plt.plot(p[0]-0.1,p[1]-0.1,'ko')
    #plt.plot(p[0]+0.1,p[1]+0.1,'ko')
    #plt.plot(p[0]-0.1,p[1]+0.1,'ko')
    #plt.plot(p[0]+0.1,p[1]-0.1,'ko')
    #plt.xlim(p[0]-0.2,p[0]+0.2)
    #plt.ylim(p[1]-0.2,p[1]+0.2)
    plt.xlim(0,0.5)
    plt.ylim(0,0.5)
    plt.show()
    
phase2()