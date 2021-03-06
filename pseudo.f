! Gerador de n?meros aleat?rios
! Provavelmente baseado em c?digos da primeira edi??o do Numerical Recipes

	program mytest1

	real RAN2  
	EXTERNAL RAN2

	IDUM= -135
	open (unit=1,file="psd.dat") 
	DO i=1,300000000
		write(1,*),real(RAN2(IDUM))
		!print *,i
	END DO
	close(1)  

	end

	FUNCTION RAN2(IDUM)
		PARAMETER (M=714025,IA=1366,IC=150889,RM=1.4005112E-6)
		DIMENSION IR(97)
		save IR, IY
		DATA IFF /0/
		IF(IDUM.LT.0.OR.IFF.EQ.0)THEN
			IFF=1
			IDUM=MOD(IC-IDUM,M)
			DO J=1,97
				IDUM=MOD(IA*IDUM+IC,M)
				IR(J)=IDUM
			END DO
			IDUM=MOD(IA*IDUM+IC,M)
			IY=IDUM
		ENDIF
		J=1+(97*IY)/M
		IF(J.GT.97.OR.J.LT.1)PAUSE
		IY=IR(J)
		RAN2=IY*RM
		IDUM=MOD(IA*IDUM+IC,M)
		IR(J)=IDUM
		RETURN
	END

