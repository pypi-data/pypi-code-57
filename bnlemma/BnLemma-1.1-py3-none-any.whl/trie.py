# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 22:50:43 2018

@author: karigor
"""


char_map = {
"u0985":'অ',
"u0986":'আ',
"u0987":'ই',
"u0988":'ঈ',
"u0989":'উ',
"u098a":'ঊ',
"u098b":'ঋ',
"u098f":'এ',
"u0990":'ঐ',
"u0993":'ও',
"u0994":'ঔ',
"u0995":'ক',
"u0996":'খ',
"u0997":'গ',
"u0998":'ঘ',
"u0999":'ঙ',
"u099a":'চ',
"u099b":'ছ',
"u099c":'জ',
"u099d":'ঝ',
"u099e":'ঞ',
"u099f":'ট',
"u09a0":'ঠ',
"u09a1":'ড',
"u09a2":'ঢ',
"u09a3":'ণ',
"u09a4":'ত',
"u09a5":'থ',
"u09a6":'দ',
"u09a7":'ধ',
"u09a8":'ন',
"u09aa":'প',
"u09ab":'ফ',
"u09ac":'ব',
"u09ad":'ভ',
"u09ae":'ম',
"u09af":'য',
"u09b0":'র',
"u09b2":'ল',
"u09b6":'শ',
"u09b7":'ষ',
"u09b8":'স',
"u09b9":'হ',
"u09dc":'ড়',
"u09dd":'ঢ়',
"u09df":'য়',
"u09ce":'ৎ',
"u0982":'ং',
"u0983":'ঃ',
"u0981":'ঁ', 
"u09be":'া',
"u09bf":'ি',
"u09c0":'ী',
"u09c1":'ু',
"u09c2":'ূ',
"u09c3":'ৃ',
"u09c7":'ে',
"u09c8":'ৈ',
"u09cb":'ো',
"u09cc":'ৌ',
"u09cd":'্',
"u09bc":'়',
"u09d7":'ৗ'}


import json
import re
class Trie:
    head = {}

    def add(self, word):
        
        cur = self.head
        for ch in word:
            if ch not in cur:
                cur[ch] = {}
            cur = cur[ch]
        # * denotes the Trie has this word as item
        # if * doesn't exist, Trie doesn't have this word but as a path to longer word
        cur['*'] = 1

    def search(self, word):
        cur = self.head
        alpha=""
        k=""
        cnt=0
        
        for ch in word:  
            if ch not in cur:
                if cnt == 0:
                    return word
                mm=""               
                for it in k: 
                    if re.search(r'[a-zA-Z0-9\d]', it):
                        mm = mm+it                      
                    if it==':':
                        alpha = alpha + char_map[mm]
                        mm=""                      
                    if it == '*':
                        return alpha
 
            cur = cur[ch]
            alpha = alpha+ch
            k = json.dumps(cur)
            cnt = cnt+1

        if '*' in cur:
            return alpha
        else:
            mm=""  
                         
            for it in k: 
                if re.search(r'[a-zA-Z0-9\d]', it):
                    mm = mm+it                      
                if it==':':
                    alpha = alpha + char_map[mm]
                    mm=""                      
                if it == '*':
                    return alpha
      
dictionary = Trie()




word = "বন্ধু-বান্ধব"

a = dictionary.search(word)
