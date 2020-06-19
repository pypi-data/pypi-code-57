# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 11:24:19 2018

@author: karigor
"""


# A Dynamic Programming based Python program for edit 
# distance problem 
def min_dis(str1, str2): 
    m = len(str1)
    n = len(str2)
    dp = [[0 for x in range(n+1)] for x in range(m+1)] 
  
  
    for i in range(m+1): 
        for j in range(n+1): 
            if i == 0: 
                dp[i][j] = j    
            elif j == 0: 
                dp[i][j] = i  
  
            elif str1[i-1] == str2[j-1]: 
                dp[i][j] = dp[i-1][j-1] 
  
            else: 
                dp[i][j] = 1 + min(dp[i][j-1],        
                                   dp[i-1][j],         
                                   dp[i-1][j-1])
  
    return dp[m][n] 
