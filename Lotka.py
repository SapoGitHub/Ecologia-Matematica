"""
Modelo de Lotka-Volterra com amortecimento
Autor: Jhordan Silveira de Borba (sbjhordan@gmail.com)
Site: https://sites.google.com/view/jdan/
"""
import matplotlib.pyplot as plt
import numpy as np

# SOLUÇÕES LOTKA VOLTERRA
def sol_lot():
    x=[]
    y=[]
    x.append(1)      # População inicial de presas
    y.append(0.5)    # População inicial de predadores
    N=400000         # Quantidade de passos
    d=0.0001         # Tamanhodos passos
    a=0              # 1: Amortecido, 0: Sem amortecimento
    
    for i in range(N-1):
        x.append(x[i]+d*(x[i]*(1-0.5*y[i])-0.5*x[i]*x[i]*a))
        y.append(y[i]+d*(y[i]*(-0.75+0.5*x[i])))
    #Plotamos a evolução temporal das frações para um caso (D,ey)
    X=np.arange(len(x)) #Eixo x
    plt.plot(X,x,'b-')
    plt.plot(X,y,'k-')
    plt.xlabel('Passo')
    plt.ylim(0,6)
    plt.show()


def phase_lot():
    #PLANO DE FASE LOTKA-VOLTERRA
    X = np.arange(0, 4, 0.2)
    Y = np.arange(0, 4, 0.2)
    U,V=np.meshgrid(X,Y)
    
    p1=[0.,0.] # Ponto de equilíbrio 1
    p2=[1.5,2.0] # Ponto de equilíbrio 1
    p3=[1.5*100,0.5*100] # Ponto de equilíbrio 1
    
    c=0
    for x in X:
        l=0
        for y in Y:
            #Distâncias
            d1=np.sqrt((x-p1[0])*(x-p1[0])+(y-p1[1])*(y-p1[1]))
            d2=np.sqrt((x-p2[0])*(x-p2[0])+(y-p2[1])*(y-p2[1]))
            d3=np.sqrt((x-p3[0])*(x-p3[0])+(y-p3[1])*(y-p3[1]))
            
            #encontrar o ponto ais próximo
            p=1
            if(d2<d1):
                p=2
                if(d3<d2):
                    p=3
            elif(d3<d1):
                p=3
                
            #Calculamos o vetor baseado no ponto mais próximo:
            if(p==1):
                a=x
                b=-0.75*y
            elif(p==2):
                a=-0.75*(y-2)
                b=x-1.5
            elif(p==3):
                a=0.75*((1.5-x)+(0.5-y))
                b=0.25*(x-1.5)
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
    plt.plot(p2[0],p2[1],'go')
    #plt.plot(p3[0],p3[1],'go')
    plt.show()

sol_lot()

