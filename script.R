#Autor: Jhordan Silveira de Borba (sbjhordan@gmail.com)
#Site: https://sites.google.com/view/jdan/

#COMPARAR OS RESULTADOS PARA ey=0.017-------------------------------------------------------------------------------------------
Dados0 <- read.table("C:\\Users\\MIkrokroft\\Google Drive\\Estudos\\Pesquisa\\Mestrado\\Dados\\evol-ey17-C05-1-015-E05-01-M20-80-D3rnd.dat")
Dados1 <- read.table("C:\\Users\\MIkrokroft\\Google Drive\\Estudos\\Pesquisa\\Mestrado\\Dados\\evol-ey17.dat")
par(mfrow=c(1,2))
plot( c(Dados0[,1]), c(Dados0[,2]), col="black", main="Original", ylab="Fração", xlab="passo" ,type="l",ylim=c(0,0.5))
lines(c(Dados0[,1]), c(Dados0[,3]), col="blue")
lines(c(Dados0[,1]), c(Dados0[,4]), col="red")
#legend("topright", c("Guanacos","Ovelhas","Pumas"), fill=c("black","blue","red"))
plot( c(Dados1[,1]), c(Dados1[,2]), col="black", main="Meu", ylab="Fração", xlab="passo" ,type="l",ylim=c(0,0.5))
lines(c(Dados1[,1]), c(Dados1[,3]), col="blue")
lines(c(Dados1[,1]), c(Dados1[,4]), col="red")
#legend("topright", c("Guanacos","Ovelhas","Pumas"), fill=c("black","blue","red"))
#CENÁRIOS DE CONFLITO-----------------------------------------------------------------------------------------------------------
BC <- read.table("C:\\Users\\MIkrokroft\\Google Drive\\Estudos\\Pesquisa\\Mestrado\\Dados\\BC.dat")
MC <- read.table("C:\\Users\\MIkrokroft\\Google Drive\\Estudos\\Pesquisa\\Mestrado\\Dados\\MC.dat")
AC <- read.table("C:\\Users\\MIkrokroft\\Google Drive\\Estudos\\Pesquisa\\Mestrado\\Dados\\AC.dat")

#MATRIZ DE ESTADO-----------------------------------------------------------------------------------------------------------------
library('tseries')
library('plot.matrix')
par(mfrow=c(1,2))
s <- read.matrix( "C:\\Users\\MIkrokroft\\Google Drive\\Estudos\\Pesquisa\\Mestrado\\Dados\\8999s.dat") 
x1 <- read.matrix("C:\\Users\\MIkrokroft\\Google Drive\\Estudos\\Pesquisa\\Mestrado\\Dados\\8999x1.dat") 
x2 <- read.matrix("C:\\Users\\MIkrokroft\\Google Drive\\Estudos\\Pesquisa\\Mestrado\\Dados\\8999x2.dat") 
y <- read.matrix( "C:\\Users\\MIkrokroft\\Google Drive\\Estudos\\Pesquisa\\Mestrado\\Dados\\8999y.dat") 
L<-100
for (i in 1:L){
	for (j in 1:L){
		if(x1[i,j]==1 || x2[i,j]==1 || y[i,j]==1){
			s[i,j]<-s[i,j]-0.5
		}
	}
}
plot(s, col=c('red', 'green', 'yellow'), breaks=c(0, 0.25,0.75, 1), key=NULL,, axis.col=NULL, axis.row=NULL, xlab='', ylab='',main='Passo 9000')   
for (i in 1:L){
	for (j in 1:L){
		a<-j
		b<-L-i+1
		if (x1[i,j]==1){
			points(a-0.25,b+0.25,pch=15)
		}
		#if (x2[i,j]==1){
		#	points(a+0.25,b+0.25,pch=16)
		#}
		if (y[i,j]==1){
			points(a,b,pch=17)
		}
	}
}

#COMPARAÇÃO DE MÉDIA DOS ASSEMBLES------------------------------------------------------------------------------------------------------------------
n<-c(1:40)/1000
par(mfrow=c(1,2))
Dados <- read.table("C:\\Users\\MIkrokroft\\Google Drive\\Estudos\\Pesquisa\\Mestrado\\Dados\\medias3.dat")
plot( n, c(Dados[,2]), col="black", main="Predação original", ylab="Fração", xlab="passo" ,type="l",ylim=c(0,1.))
lines(n, c(Dados[,3]), col="blue")
lines(n, c(Dados[,4]), col="red")
#legend("topright", c("Guanacos","Ovelhas","Pumas"), fill=c("black","blue","red"))

#EVOLUÇÃO TEMPORAL 2015---------------------------------------------------------------------------------------------------------------------
Dados <- read.table("C:\\Users\\MIkrokroft\\Google Drive\\Estudos\\Pesquisa\\Mestrado\\Dados\\temporal2019.dat")

#EVOLUÇÃO TEMPORAL 2019---------------------------------------------------------------------------------------------------------------------
Dados1 <- read.table("C:\\Users\\MIkrokroft\\Google Drive\\Estudos\\Pesquisa\\Mestrado\\Dados\\2019\\temporal20191.dat")
Dados2 <- read.table("C:\\Users\\MIkrokroft\\Google Drive\\Estudos\\Pesquisa\\Mestrado\\Dados\\2019\\temporal20192.dat")
Dados3 <- read.table("C:\\Users\\MIkrokroft\\Google Drive\\Estudos\\Pesquisa\\Mestrado\\Dados\\2019\\temporal20193.dat")
Dados4 <- read.table("C:\\Users\\MIkrokroft\\Google Drive\\Estudos\\Pesquisa\\Mestrado\\Dados\\2019\\temporal20194.dat")
Dados5 <- read.table("C:\\Users\\MIkrokroft\\Google Drive\\Estudos\\Pesquisa\\Mestrado\\Dados\\2019\\temporal20195.dat")
Dados6 <- read.table("C:\\Users\\MIkrokroft\\Google Drive\\Estudos\\Pesquisa\\Mestrado\\Dados\\2019\\temporal20196.dat")
Dados7 <- read.table("C:\\Users\\MIkrokroft\\Google Drive\\Estudos\\Pesquisa\\Mestrado\\Dados\\2019\\temporal20197.dat")
Dados8 <- read.table("C:\\Users\\MIkrokroft\\Google Drive\\Estudos\\Pesquisa\\Mestrado\\Dados\\2019\\temporal20198.dat")
Dados9 <- read.table("C:\\Users\\MIkrokroft\\Google Drive\\Estudos\\Pesquisa\\Mestrado\\Dados\\2019\\temporal20199.dat")
par(mfrow=c(1,2))
plot( c(Dados1[4000:6000,1]), c(Dados1[4000:6000,2]), col="green", main="Guanacos", ylab="Fração", xlab="passo" ,type="l",ylim=c(0,.8))
lines(c(Dados1[4000:6000,1]), c(Dados2[4000:6000,2]),col = "aquamarine")
lines(c(Dados1[4000:6000,1]), c(Dados3[4000:6000,2]),col = "cadetblue")
lines(c(Dados1[4000:6000,1]), c(Dados4[4000:6000,2]),col = "blue")
lines(c(Dados1[4000:6000,1]), c(Dados5[4000:6000,2]),col = "purple")
lines(c(Dados1[4000:6000,1]), c(Dados6[4000:6000,2]),col = "pink")
lines(c(Dados1[4000:6000,1]), c(Dados7[4000:6000,2]),col = "palevioletred3")
lines(c(Dados1[4000:6000,1]), c(Dados8[4000:6000,2]),col = "red")
lines(c(Dados1[4000:6000,1]), c(Dados9[4000:6000,2]),col = "black")
plot( c(Dados1[4000:6000,1]), c(Dados1[4000:6000,3]),col="green", main="Ovelha", ylab="Fração", xlab="passo" ,type="l",ylim=c(0,.8))
lines(c(Dados1[4000:6000,1]), c(Dados2[4000:6000,3]),col = "aquamarine")
lines(c(Dados1[4000:6000,1]), c(Dados3[4000:6000,3]),col = "cadetblue")
lines(c(Dados1[4000:6000,1]), c(Dados4[4000:6000,3]),col = "blue")
lines(c(Dados1[4000:6000,1]), c(Dados5[4000:6000,3]),col = "purple")
lines(c(Dados1[4000:6000,1]), c(Dados6[4000:6000,3]),col = "pink")
lines(c(Dados1[4000:6000,1]), c(Dados7[4000:6000,3]),col = "palevioletred3")
lines(c(Dados1[4000:6000,1]), c(Dados8[4000:6000,3]),col = "red")
lines(c(Dados1[4000:6000,1]), c(Dados9[4000:6000,3]),col = "black")
legend(-.35,1.5, c("5","11","21","30","40","50","60","75","80"), fill=c("aquamarine","cadetblue","blue","purple","pink","palevioletred3","red","black"))

#Raízes equação tanscendental
#MATRIZ DE ESTADO-----------------------------------------------------------------------------------------------------------------
library('tseries')
library('plot.matrix')
m <- read.matrix( "C:\\Users\\MIkrokroft\\Google Drive\\Estudos\\Pesquisa\\Mestrado\\Dados\\Raizes.dat") 
m<-t(m)
m <-m[90:2, 1:35]
rownames(m) <- (99:11)/10
colnames(m) <- (0:34)/10
plot(m, col=c('black', 'white', 'green'), breaks=c(-2, -0.25,0.25, 2), xlab='R1', ylab='R0',main='Raizes',border=NA)   

------------------
par(mfrow=c(1,1))
M <- read.table("C:\\Users\\MIkrokroft\\Documents\\GitHub\\Ecologia-Matematica\\C# Tutorial\\Vida selvagem e Pecuária\\bin\\Debug\\Dados.dat")
plot( c(M[,1]), c(M[,2]), col="black", main="Quantidade de indivíduos", ylab="", xlab="passo" ,type="l",ylim=c(0,5000.))
lines(c(M[,1]), c(M[,3]), col="blue")
lines(c(M[,1]), c(M[,4]), col="red")