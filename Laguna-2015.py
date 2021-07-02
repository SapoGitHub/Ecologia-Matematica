# -*- coding: UTF-8 -*-
"""
Autor: Jhordan Silveira de Borba (sbjhordan@gmail.com)
Site: https://sites.google.com/view/jdan/
"""

#Bibliotecas
import numpy as np                                      # Biblioteca de funções matemáticas
import copy                                             # Biblioteca com funções para copiar

#Salvar a situação final de cada matriz
def inst(c,s,x1,x2,y):
    f = open(str(c)+"s.dat", "w")
    for i in s:
        for j in i:
            f.write(str(j)+"	")
        f.write("\n")
    f.close()

    f = open(str(c)+"x1.dat", "w")
    for i in x1:
        for j in i:
            f.write(str(j)+"	")
        f.write("\n")
    f.close()
        
    f = open(str(c)+"x2.dat", "w")
    for i in x2:
        for j in i:
            f.write(str(j)+"	")
        f.write("\n")
    f.close()
        
    f = open(str(c)+"y.dat", "w")
    for i in y:
        for j in i:
            f.write(str(j)+"	")
        f.write("\n")
    f.close()
    
    return

#CONDIÇÕES INICIAIS ------------------------------------------------------
maxt = 5000     #tiempo total de cada realizacion
Lx   = 100      #tamaño del sustrato
Ly   = 100

#Fracciones iniciales
D    = 0.3          #fraccion inicial de sitios destruidos
x10  = 0.5          #fraccion inicial de sitios ocupados por x1
x20  = 0.5          #fraccion inicial de sitios ocupados por x2
y0   = 0.5          #fraccion inicial de sitios ocupados por y

#Tasas               
cx1   = 0.05         #colonizaciones       
cx2   = 0.1        
cy    = 0.015     
ex1   = 0.05         #extinciones       
ex2   = 0.01      
eyi   = 0.001
eyf   = 0.04
mx1y  = 0.2          #depredaciones       
mx2y  = 0.8            
depx1 = ex1+mx1y       #mortalidad aumentada=extincion+depredacion
depx2 = ex2+mx2y

#Configurações de simulações
S     = 1          # Quantidade de simulações que vamos tirar a média
M     = 2000       # Quantidade de passos finais que vamos obter a médiaa
R     = 50000      # Passo que vamos remover as ovelhas

rng = np.random.RandomState(2021) #Define os números pseudo-aleatórios

f1 = open("medias.dat", "w")
f2 = open("desvio_padrao.dat", "w")

for EY in range(int(eyi*1000),int(eyf*1000)+1,1): # Percorrer os fatores de extinção local do puma
    ey=float(EY)/1000  # Os passos são de 0.001
    print("Extincao local: "+str(ey))   # Printa o fator ey atual

    #Listas para guardar os % das N simulações para o mesmo valor de ey
    ovelhas=[]  # Lista para guardar a % de fragmentos com ovelhas
    guanacos=[] # Lista para guardar a % de fragmentos com guancamos
    pumas=[]    # Lista para guardar a % de fragmentos com pumas

    for sim in range(S):  # Realiza a quantidade de simulações estipuladas para cada valor de ey
        print("Simulacao: "+str(sim+1))       # Printa qual é a atual simulação
      
        #Listas para guardar a evolução temporal de cada simulação
        oe=[]       # Fragmentos com ovelhas
        ge=[]       # Fragmentos com guancamos
        pe=[]       # Fragmentos com pumas

        #Inicializaciones
        s  = np.full((Lx, Ly), [1])   #matriz de habitat (1=sitio disponible, 0=destruido)
        x1 = np.full((Lx, Ly), [0])   #1 = sitio ocupado, 0 sitio vazio
        x2 = np.full((Lx, Ly), [0])   #1 = sitio ocupado, 0 sitio vazio
        y  = np.full((Lx, Ly), [0])   #1 = sitio ocupado, 0 sitio vazio

        for i in range(1,Lx-1): 
          for j in range (1,Ly-1): 
            rnd=rng.rand()
            if (rnd < D): s[i,j]=0
            rnd=rng.rand()
            if (rnd < x10 and s[i,j]==1): x1[i,j]=1
            rnd=rng.rand()
            if (rnd < x20 and s[i,j]==1): x2[i,j]=1
            rnd=rng.rand()
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
        oe.append(fx2);ge.append(fx1);pe.append(fy) 
        f3 = open("temporal.dat", "w")
        f3.write(str(0)+"	"+str(fx1)+"	"+str(fx2)+"	"+str(fy)+"\n")

        for it in range(maxt):
            if (float(it)%(float(maxt)/100)==0.):
                print("Porcentagem: "+str(it*100/maxt))  # Exibe o passo atual

            # Todas ovelhas são removidas no passo R e os parâmetros atualizados
            if (it==R):
                inst(it,s,x1,x2,y)
                x2 = np.full((Lx, Ly), [0])  
                cx1   = 0.1    
                ex1   = 0.025         
                ey    = 0.015
                mx1y  = 0.3                
                depx1 = ex1+mx1y  

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
                      rnd=rng.rand() 
                      if (rnd < p):x1[i,j]=1
                    
                    if (x2old[i,j]==0 and s[i,j]==1 and x1old[i,j]==0):         #colonizacion de x2 si el sitio esta libre de x1 y x2, y no destruido: 
                      nvec=x2old[i-1,j]+x2old[i+1,j]+x2old[i,j-1]+x2old[i,j+1]  #cantidad de vecinos ocupados
                      p=1.0-(1.0-cx2)**nvec                                     #probabilidad de ser colonizado= 1 - prob de quedar libre 
                      rnd=rng.rand()
                      if (rnd < p): x2[i,j]=1                                
          
                    ocup=0                                                       #ocupacion de herbivoros 
                    if (x1old[i,j]==1 or x2old[i,j]==1): ocup=1
                    if (yold[i,j]==0 and ocup==1):                               #colonizacion de y si el sitio está libre de y,y ocupado por un x 
                      nvec=yold[i-1,j]+yold[i+1,j]+yold[i,j-1]+yold[i,j+1]       #cantidad de vecinos ocupados
                      p=1.0-(1.0-cy)**nvec                                       #probabilidad de ser colonizado= 1 - prob de quedar libre 
                      rnd=rng.rand()
                      if (rnd < p): y[i,j]=1
          
                    #extinciones sin depredadores
                    if (x1old[i,j]==1 and yold[i,j]==0):                          #extincion de x1 si el sitio esta ocupado 
                      rnd=rng.rand()
                      if (rnd < ex1): x1[i,j]=0
          
                    if (x2old[i,j]==1 and yold[i,j]==0):                          #extincion de x2 si el sitio esta ocupado 
                      rnd=rng.rand()
                      if (rnd < ex2): x2[i,j]=0
          
                    if (yold[i,j]==1):                                            #extincion de y si el sitio esta ocupado 
                      rnd=rng.rand()
                      if (rnd < ey): y[i,j]=0

                    #depredacion (extinción de presas donde hay depredadores)
                    if (x1old[i,j]==1 and yold[i,j]==1):                          #depredacion de y sobre x1 
                      rnd=rng.rand()
                      if (rnd < depx1): x1[i,j]=0
            
                    if (x2old[i,j]==1 and yold[i,j]==1):                          #depredacion de y sobre x2 
                      rnd=rng.rand()
                      if (rnd < depx2): x2[i,j]=0
                      
                    #MI OPCIÓN
                    #extinciones sin depredadores
                    # if (x1old[i,j]==1):                          #extincion de x1 si el sitio esta ocupado 
                    #   rnd=rng.rand()
                    #   if (rnd < ex1): x1[i,j]=0

                    # if (x2old[i,j]==1):                          #extincion de x2 si el sitio esta ocupado 
                    #   rnd=rng.rand()
                    #   if (rnd < ex2): x2[i,j]=0

                    # if (yold[i,j]==1):                                            #extincion de y si el sitio esta ocupado 
                    #   rnd=rng.rand()
                    #   if (rnd < ey): y[i,j]=0

                    # #depredacion (extinción de presas donde hay depredadores)
                    # if (x1old[i,j]==1 and yold[i,j]==1):                          #depredacion de y sobre x1 
                    #   rnd=rng.rand()
                    #   if (rnd < mx1y): x1[i,j]=0
            
                    # if (x2old[i,j]==1 and yold[i,j]==1):                          #depredacion de y sobre x2 
                    #   rnd=rng.rand()
                    #   if (rnd < mx2y): x2[i,j]=0
            
                    #desplazamiento por competencia (jerarquia)
                    if (x1old[i,j]==1 and x2old[i,j]==1):
                      rnd=rng.rand()
                      if (rnd < cx1): x2[i,j]=0
                    #Termina a célula
                #Termina a linha
      
            fx1=sum(sum(x1))/((Lx-1)*(Ly-1))
            fx2=sum(sum(x2))/((Lx-1)*(Ly-1))
            fy =sum(sum(y)) /((Lx-1)*(Ly-1))
            oe.append(fx2);ge.append(fx1);pe.append(fy) 
            f3.write(str(it+1)+"	"+str(fx1)+"	"+str(fx2)+"	"+str(fy)+"\n") # Salvamos a situaçaõ do passo
            #Termina o laço temporal

        # Ao final da simulação ################################################
        f3.close
        ovelhas.append( np.array(oe[-M:]).mean())
        guanacos.append(np.array(ge[-M:]).mean())
        pumas.append(   np.array(pe[-M:]).mean())    
          
    # CÁLCULOS FINAIS -----------------------------------------------------
    f1.write(str(EY/1000)+"	"+str(np.array(guanacos).mean())+"	"+str(np.array(ovelhas).mean())+"	"+str(np.array(pumas).mean())+"\n")
    f2.write(str(EY/1000)+"	"+str( np.array(guanacos).std())+"	"+str( np.array(ovelhas).std())+"	"+str( np.array(pumas).std())+"\n")

f1.close()
f2.close()

#inst(it,s,x1,x2,y)
