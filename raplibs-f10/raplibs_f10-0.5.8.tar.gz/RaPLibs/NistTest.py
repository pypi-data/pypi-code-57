import scipy.special as sp
import numpy as np
import math 


def MonoBit_Block(Sequence,M):


    n=len(Sequence);
    N=int(n/M);
    bp=np.arange(1,N);
    nel=N*M;
    
    e_matr=np.reshape(Sequence[0:nel],(N,M));
    
    chi=0;
    for i in np.arange(0,N-1):
        block_p = sum(e_matr[i,:]);
        bp[i]=block_p/M
        chi=chi+(bp[i]-0.5)**2;
    
    
    chi_Tot=4*M*chi;    
    pval = sp.gammainc(chi_Tot/2,N/2);
    print('Monobit:' + str(pval))
    if np.isnan(pval):
        pval=0
    
    return pval




def MonoBit(Sequence):

    SS=0;
    for i in np.arange(0,len(Sequence)):
        if Sequence[i]==1:
            SS=SS+1
        else:
            SS=SS-1
   
    
    sn=abs(SS)/math.sqrt(len(Sequence))
    pval=sp.erfc(sn);
    #print('Monobit:' + str(pval))
    
    if np.isnan(pval):
        pval=0
    
    return pval


def RunsTest(Sequences):

    prop=sum(Sequences);
    prop=prop/len(Sequences);
    t=2/math.sqrt(len(Sequences));
    
    if abs(prop-0.5) >= t:
        pval=0
    else:
    
        Vobs=0;
    
        for i in np.arange(0,len(Sequences)-1):
            if Sequences[i] != Sequences[i+1]:
                Vobs=Vobs+1;
    
        Vobs=Vobs+1;
        
        Sup1=Vobs;
        Sup2=2*len(Sequences)*prop*(1-prop);
        Den=2*prop*(1-prop)*math.sqrt(2*len(Sequences))
        #print('Sup1:' + str(Sup1))
        #print('Sup2:' + str(Sup2))
        #print('Den:' + str(Den))
    
                                      
        pval = sp.erfc( abs(Sup1-Sup2)/Den )
            
    #print('Runs:' + str(pval))
    return pval
    


    
    
    
    
    
    
    
    
    
    
    