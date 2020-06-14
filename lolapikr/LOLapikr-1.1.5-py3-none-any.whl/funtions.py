# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 01:53:30 2020

@author: dhk1349
"""
import json
#필요한 함수

def GetChampiondict():
    with open('champion.json',encoding='UTF8') as json_file:
        champion_parser = json.load(json_file)['data']
    champion={}
    for name, data in champion_parser.items():
        champion[str(data['key'])]=name
    return champion
    
def GameDataParser(path):
    #Output으로 받은 txt파일을 파싱하는 함수 
    #각 줄의 형식
    #게임 id | 100,aa,bb,cc|200,aa,bb,cc|win, loss
    f=open(path, 'r')
    line=f.readline()
    output=[]
    while (line):
        row=[]
        for i in line.split('|'):
            row.append(i.split(','))
        output.append(row)
        line=f.readline()
    return output

"""
Champs=GetChampiondict()
for num, name in Champs.items():
    print(num+": "+name)
#print(GameDataParser("C:/Users/dhk13/Documents/GitHub/League_of_Legend_4U/lolapi/gamedata0609.txt"))
print(GameDataParser("C:/Users/dhk13/Documents/GitHub/League_of_Legend_4U/lolapi/ChallengerDiv0609.txt"))
"""