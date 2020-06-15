#!/usr/bin/env python
# coding: utf-8

# In[2]:


def fileread(filename) : 
    f = open(filename, 'r')
    while True:
        line = f.readline()
        print(line)
        if not line: break
    f.close()


# In[ ]:




