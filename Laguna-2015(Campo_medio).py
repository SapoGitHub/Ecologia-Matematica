"""
Autor: Jhordan Silveira de Borba (sbjhordan@gmail.com)
Site: https://sites.google.com/view/jdan/
"""

import numpy as np                                      # Biblioteca de funções matemáticas
import matplotlib.pyplot as plt   
from matplotlib.colors import LinearSegmentedColormap
 
#Parâmetros

M=4
c1=M*0.05                # Fator de colonização do guancamo 
c2=M*0.1                 # Fator de colonização da ovelha
cy=M*0.015               # Fator de colonização do puma
e1=0.05                  # Fator de extinção local do guancamo
e2=0.01                  # Fator de extinção local da ovelha
EY0=0.02                 # Fator de extinção local do puma
u1=0.2                   # Fator de predação do guancamo
u2=0.8                   # Fator de predação da ovelha
N=int(200000)#+300000)
F=100 
d=0.01

#Variáveis
D0=0.4
D1=D0
EY1=EY0


X1=[]
X2=[]
YP=[]

#passo que vamos remover as ovelhas
R=int(N)#-200000)

for DD in range(int(D0*F),int(D1*F)+1,1):
    D=DD/F
    #As linhas
    X1L=[]
    X2L=[]
    YL=[]
    for EY in range(int(EY0*10*F),int(EY1*10*F)+1,1):#(0,41,1): # Percorrer os fatores de extinção local do puma
        ey=EY/(10*F)
        print(str(D)+","+str(ey))
        #para cada simulação
        # Criar as listas
        x1=[]
        x2=[]
        y=[]
        #Valores iniciais:
        x1.append(0.2)
        x2.append(0.2)
        y.append(0.2)
        for i in range(N-1):
            # if (i==R):
            #     c1=c1*2
            #     e1=e1/2
            #     EY0=EY0*0.75
            #     EY1=EY0
            #     u1=u1*1.5
            #     x2[i]=0

            #Sistema de equações diferenciais originais
            a=x1[i]+d*(c1*x1[i]*(1-D-x1[i])-e1*x1[i]-u1*x1[i]*y[i])
            x1.append(a)
            #x2.append(x2[i]+d*(c2*x2[i]*(1-D-x1[i]-x2[i])-e2*x2[i]-u2*x2[i]*y[i]-c1*x1[i]*x2[i]))
            #y.append(y[i]+d*(cy*y[i]*(x1[i]+x2[i]-x1[i]*x2[i]-y[i])-ey*y[i]))
            #Meu sistema
            x2.append(x2[i]+d*(c2*x2[i]*(1-D-x1[i]-x2[i]+x1[i]*x2[i])-e2*x2[i]-u2*x2[i]*y[i]-c1*x1[i]*x2[i]))
            y.append(y[i]+d*(cy*y[i]*(x1[i]+x2[i]-x1[i]*x2[i]-y[i]*(x1[i]+x2[i]-x1[i]*x2[i]))-ey*y[i]))
        X1L.append(x1[N-1])
        X2L.append(x2[N-1])
        YL.append(y[N-1])
    X1.append(X1L)
    X2.append(X2L)
    YP.append(YL)

#Plotamos a evolução temporal das frações para um caso (D,ey)    
def tmp(x1,x2,y,D0):
    x=np.arange(len(x1)) #Eixo x
    plt.plot(x,x2,'b-')
    plt.plot(x,x1,'k-')
    plt.plot(x,y,'r-')
    plt.ylabel('Fração ocupada')
    plt.xlabel('Passo')
    plt.ylim(0,0.35)
    plt.title("D="+str(D0))
    plt.show()

# Variando D e ey
def grafico3D (a,e,X1,X2,YP):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    X=np.arange(len(X1))
    Y=X
    X, Y = np.meshgrid(X, Y)
    Z1=np.array(X1)
    Z2=np.array(X2)
    Z3=np.array(YP)
    ver = LinearSegmentedColormap.from_list("CMAP", [(1, 0, 0),(1,0,0)], N=1)
    azu = LinearSegmentedColormap.from_list("CMAP", [(0, 0, 1),(0,0,1)], N=1)
    pre = LinearSegmentedColormap.from_list("CMAP", [(0, 0, 0),(0,0,0)], N=1)
    ax.plot_surface(X, Y, Z1, cmap=pre)#, linewidth=0, antialiased=False)
    ax.plot_surface(X, Y, Z2, cmap=azu)#, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    ax.plot_surface(X, Y, Z3, cmap=ver)#, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    ax.set_xlim(0, len(X)-1)
    ax.set_ylim(0, len(X)-1)
    #ax.set_zlim(0, 0.1)
    ax.view_init(azim=a,elev=e)
    ax.set_xlabel("ey")
    ax.set_ylabel("D")
    plt.show()

# Variar ey com D fixo
def VEY(X1,X2,YP):
    x2=X2[0]
    x1=X1[0]
    y=YP[0]
    x=np.arange(len(x1)) #Eixo x
    plt.plot(x,x2,'b-')
    plt.plot(x,x1,'k-')
    plt.plot(x,y,'r-')
    plt.ylabel('Fração ocupada')
    plt.xlabel('ey')
    plt.show()
    

# Variar D com ey fixo
def VD(X1,X2,YP):
    x2=[]
    x1=[]
    y=[]
    for i in range(len(X1)):
        x1.append(X1[i][0])
        x2.append(X2[i][0])
        y.append(YP[i][0])
    x=np.arange(len(x1)) #Eixo x
    plt.plot(x,x2,'b-')
    plt.plot(x,x1,'k-')
    plt.plot(x,y,'r-')
    plt.ylabel('Fração ocupada')
    plt.xlabel('D')
    plt.show()
    
tmp(x1,x2,y,D0)
