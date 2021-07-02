"""
Autor: Jhordan Silveira de Borba (sbjhordan@gmail.com)
Site: https://sites.google.com/view/jdan/
"""
import matplotlib.pyplot as plt
import numpy as np


#Função para resolver o sistema de equações diferenciais
def sistema(R0,R1):
    #Parâmetro R0=b.ti
    #Parâmetro R1=tr/ti
    
    #Parâmetros da dinâmica
    b =4
    ti=R0/b
    tr=R1*R0/b
    to=ti+tr
    
    # Listas para guardar a evolução do sistema
    s=[]
    i=[]
    
    d=0.001 #Passo para o método de Euler
    
    #Primeira parte:
    N1=int(ti/d)     #Quantidade de passos
    i.append(1e-16)  #Condição inicial de inectado i0
    s.append(1-i[0]) #Condição inicial de suscetíveis s0=1-i0
        
    #Resolve o sistema Usando o método de Euler
    for k in range(N1):
        s.append(s[k]+d*(-b*s[k]*i[k]))
        i.append(i[k]+d*(b*s[k]*i[k]))
    
    #Segunda parte
    N2=int(to/d)
    for k in range(N1,N2):
        s.append(s[k]+d*(-b*s[k]*i[k]))
        i.append(i[k]+d*(b*s[k]*i[k]-b*s[k-int(ti/d)]*i[k-int(ti/d)]))
    
    #Terceira parte
    N3=int(1800/d)
    for k in range(N2,N3):
        s.append(s[k]+d*(-b*s[k]*i[k]+b*s[k-int(to/d)]*i[k-int(to/d)]))
        i.append(i[k]+d*(+b*s[k]*i[k]-b*s[k-int(ti/d)]*i[k-int(ti/d)]))
        
    #Plotar a evolução inteira
    X=np.arange(len(i)) #Eixo x
    plt.plot(X,i,'k-')
    plt.xlabel('Passo')
    plt.ylim(0,1)
    plt.show()
    
    #Plotar o período 2to final
    n=int(2*to/d)
    X=np.arange(n) #Eixo x
    plt.plot(X,i[len(i)-n:],'k-')
    plt.xlabel('Passo')
    plt.ylim(0.,1.)
    plt.show()

    #Valores máximos e mínimo de oscilção durante 2to final
    print(min(i[len(i)-2*n:]))
    print(max(i[len(i)-2*n:]))
    

#Função para resolver a equação transcendental
def raizes():
    sol=np.zeros((35,90)) # Matriz para guardar as raízes
    err=1e-16             # Erro admitido
    
    sy=0
    for R0 in np.arange(1,10,0.1):      #Percorrer os valores RO=b.
        print(str(100*(sy+1)/90)+"%")
        sx=0
        for R1 in np.arange(0,3.5,0.1): #Percorrer os valores R1=tr/ti
    
            #Parâmetros da dinâmica
            b =4
            ti=R0/b
            tr=R1*R0/b
            to=ti+tr
            
            #Pontos de equilíbrio
            io=(b*ti-1)/(b*to)
            so=1/(b*ti)
            
            #Matriz das raízes para os parâmetros atuais
            r=np.zeros((20, 20))
            
            #Os chutes iniciais serão pontos dentro da malha [-1,1] em 2D
            m=0
            for a in np.arange(-1,1,0.1):
                n=0
                for y in np.arange(-1,1,0.1):
                    i=y*1j
                    x=a+i  # Ponto inicial
                    N=100000000 # Quantidade máxima de aproximações
                    #Valor da função para o chute inicial
                    f=x+b*(so*(np.power(np.e,-x*ti)-1)-io*(np.power(np.e,-x*to)-1))
                    for k in range(N):
                        if (k==N-2):
                            print("!") #Indicando que chegou no último passo sem achar a raízs
                        if (abs(f)<err):
                            break        # Se chou a raíz, do loop
                        try:
                            f =x+b*(so*(np.power(np.e,-x*ti)-1)-io*(np.power(np.e,-x*to)-1))
                            df=1+b*(to*io*np.power(np.e,-x*to)-ti*so*np.power(np.e,-x*ti))
                            nx=x-f/df        # Próximo chute
                            x=nx
                        except:
                            print(str(R0)+","+str(R1))
                            break
                    if(abs(np.real(x))<err):   # A raíz é zero
                        r[m,n]=0
                    elif (np.real(x)>0):        # Raíz positiva
                        r[m,n]=1
                        break
                    else:
                        r[m,n]=-1               # Raíz negativa
                    n=n+1
                else:        # Quando acabar o loop interno
                    m=m+1
                    continue # Continua
                break        # Se o loop interno foi encerrado antes da hora, encerra o externo
                
            res=[]        
            for i in range(20):
                res.append(max(r[i]))
            sol[sx,sy]=max(res)                 # Se houve raíz positiva, obtém.
            sx=sx+1
        sy=sy+1
    
    #Registra
    f = open("raizes.dat", "w")
    for i in sol:
         for j in i:
             f.write(str(j)+"	")
         f.write("\n")
    f.close()

raizes()
