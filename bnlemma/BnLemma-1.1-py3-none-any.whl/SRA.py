# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 22:20:46 2018

@author: karigor
"""



    
      
def RA(t_w, mp_word):
    
    l_w = len(t_w)
    k=0
    p_w = t_w
    mx=0
    for i in range(l_w):
        
        c_w = t_w[k:]
        l_n = l_w-k
        k=k+1
        
        for j in range(l_n):
            if c_w in mp_word.keys():
                l = len(c_w)
                if l>mx:
                    p_w = c_w
                    mx=l
            c_w=c_w[0:l_n-j-1]

    return p_w