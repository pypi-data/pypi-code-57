# -*- coding: utf-8 -*-
"""
Created on Sun May 17 19:56:27 2020

@author: dhk13
"""
import requests
import time
import json

"""
with open('champion.json',encoding='UTF8') as json_file:
    champion_parser = json.load(json_file)['data']
champion={}
for name, data in champion_parser.items():
    champion[str(data['key'])]=name

"""



def GetSummonerInfo(summoner_name , api_key):
    res = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" +summoner_name +'?api_key=' + api_key
    r = requests.get(res)
    tier_url = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" + r.json()['id'] +'?api_key=' + api_key
    r2  = requests.get(tier_url)
    #print(r2.json())
    if(r2.status_code==200):
        #print(sorted(r.json()['entries'], key=lambda summoner:summoner['leaguePoints'], reverse=True))
        return (r.json())
    elif(r2.status_code==429):
        time.sleep(10)
        return GetSummonerInfo(summoner_name , api_key)
    else:
        time.sleep(10)
        print("Check api key or other problems.")
        GetSummonerInfo(summoner_name , api_key)
    
def GetSummonerInfoByEnc_Id(Id, api_key):
    res1="https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" +Id +'?api_key=' + api_key
    
    res2 = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/" +Id +'?api_key=' + api_key
    r1 = requests.get(res1)
    r2  = requests.get(res2)
    
    #print(r2.json())
    if(r2.status_code==200):
        #print(sorted(r.json()['entries'], key=lambda summoner:summoner['leaguePoints'], reverse=True))
        return (r1.json(),r2.json())
    elif(r2.status_code==429):
        time.sleep(10)
        return GetSummonerInfoByEnc_Id(Id, api_key)
    else:
        time.sleep(10)
        print("Check api key or other problems.")
        return GetSummonerInfoByEnc_Id(Id, api_key)

#GetSummonerInfo(summoner, api_key)
    
def GetDivInfo(queue="RANKED_SOLO_5X5", tier= "DIAMOND", division=1, api_key=None):
    #[RANKED_SOLO_5x5, RANKED_FLEX_SR, RANKED_FLEX_TT]
    #[DIAMOND, PLATINUM, GOLD, SILVER, BRONZE, IRON]
    #[I, II, III, IV]
    res = "https://kr.api.riotgames.com/lol/league/v4/entries/"+queue+"/"+tier+"/"+division+'?api_key='+api_key
    r=requests.get(res)
    if(r.status_code==200):
        #print(sorted(r.json()['entries'], key=lambda summoner:summoner['leaguePoints'], reverse=True))
        return r.json()
    elif(r.status_code==429):

        return False
    else:

        print("Check api key or other problems.")
    #print(r.json())
    
"""
r=GetDivInfo(queue='RANKED_SOLO_5x5', tier= 'BRONZE', division='III',api_key=api_key)
for i in range(len(r)):
    print(r[i]['summonerName'])
"""
    
def GetChallengerDiv(api_key):
    res = "https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"+'?api_key='+api_key
    r=requests.get(res)
    if(r.status_code==200):
        #print(sorted(r.json()['entries'], key=lambda summoner:summoner['leaguePoints'], reverse=True))
        return sorted(r.json()['entries'], key=lambda summoner:summoner['leaguePoints'], reverse=True)
    elif(r.status_code==429):
        time.sleep(10)
        print("waiting")
        return GetChallengerDiv(api_key)
    else:
        time.sleep(10)
        print("Check api key or other problems.")
        return GetChallengerDiv(api_key)
        
"""
result=GetChallengerDiv(api_key)
for i in result:
    print(i['leaguePoints'])
"""

def GetEncId(sumname, api_key):
    res = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+sumname+'?api_key='+api_key
    r=requests.get(res)
    #print(r.json())
    if(r.status_code==429):
        print("waiting")
        time.sleep(10)
        return GetEncId(sumname, api_key)
    elif(r.status_code==200):
        enc_id=r.json()['accountId']
        return enc_id
    else:
        print(r.status_code)
        
def GetMachList(enc_acc_id, api_key):
    res = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/"+enc_acc_id+'?api_key='+api_key
    r=requests.get(res)
    if(r.status_code==200):
        result=[]
        for i in r.json()['matches']:
            if(i['queue']==420):
                result.append(i)
        
        return result
    elif(r.status_code==429):
        time.sleep(10)
        print("waiting")
        return GetMachList(enc_acc_id, api_key)
    elif(r.status_code==504):
        print("504 Gateway timeout")
        time.sleep(60)
        return GetMachList(enc_acc_id, api_key)
    else:
        print(r.status_code)
        print("Check api key or other problems.")
        time.sleep(60)
        return GetMachList(enc_acc_id, api_key)
            
    
def GetMatchData(match_id, api_key):
    res = "https://kr.api.riotgames.com/lol/match/v4/matches/"+str(match_id)+'?api_key='+api_key
    r=requests.get(res)
    if(r.status_code==200):
        return r.json()
    elif(r.status_code==429):
        time.sleep(10)
        print("waiting")
        return GetMatchData(match_id, api_key)
    elif(r.status_code==504):
        print("504 Gateway timeout")
        time.sleep(60)
        return GetMatchData(match_id, api_key)
    else:
        print(r.status_code)
        print("Check api key or other problems.")
        time.sleep(60)
        return GetMatchData(match_id, api_key)
        
def ChallengerDivTable(api_key, option):
    chall=GetChallengerDiv(api_key)
    result=[]
    print(len(chall), " of challengers detected")
    for i in chall:
        elem=""
        elem=elem+str((GetEncId(i['summonerName'], api_key)))+"|"
        elem=elem+str(i['summonerId'])+"|"
        elem=elem+str(i['summonerName'])+"|"
        elem=elem+str(i['rank'])+"|"
        elem=elem+str(i['leaguePoints'])+"|"
        result.append(elem)
        print(elem)
    if option=="-t":
        f=open("ChallengerDiv0609.txt", "w")
        for i in result:
            f.write(str(i)+"\n")
        f.close()
    return result

def MatchDataTable(inputs,api_key):
    #Enc_ID, Match_ID, Champion, Result
    f=open("gamedata0609.txt", "w")
    result=[]
    matchlist=set()
    exitbool=False
    for i in inputs:
        #enc_acc_id=i['summonerId']    
        enc_acc_id=i
        l=GetMachList(enc_acc_id, api_key)
        print(len(l), "of matchlists detected")
        for j in l:
            #print(j['gameId'])
            #f.write(str(j['gameId'])+"\n")
            matchlist.add(j['gameId'])
            if(len(matchlist)==2000):
                exitbool=True
        if(exitbool):
            break;
    print(len(matchlist),"of matches detected in total")
    elem=[0,0,0]
    for j in matchlist:
        GameData=GetMatchData(j, api_key)
        # print(GameData)
        #저장방
        #게임 id | 100,aa,bb,cc|200,aa,bb,cc|win, loss
        elem=""
        elem=elem+str(j)+"|"
        for k in range(len(GameData['participants'])):
            if(k==5):
                elem=elem+"|"
            elem=elem+str(GameData['participants'][k]['championId'])+","
        elem=elem+"|"
        for k in GameData['teams']:
            elem=elem+str(k['win'])+","
        result.append(elem)
        print (elem)
        f.write(str(elem)+"\n")
    f.close()
    return result
#chalenckey=["RCccsD-o33FTLi_VMk-hNKCkojWvXWV5W8gKCgMtnk_yb5OF7JoyW-78",'eqfglHsSwSl-Fh0ngiZdowI6CinBw6CYhzQPTIngwvs','sYfPGpcXWexXL2rtLx9VgKtQffsu2fXpJBWB_ENuFQBIV8w','g4wToX2XzT-XNpGn2wzbRPawkQxHFmbvB-qfaNDqmDR9WAM']
#print(GetMachList("RCccsD-o33FTLi_VMk-hNKCkojWvXWV5W8gKCgMtnk_yb5OF7JoyW-78", "RGAPI-4ee81316-3c0d-446f-8072-dae173fd2961"))

"""
ChallengerDivTable("RGAPI-6014d53d-88ea-4390-a23a-8c96fe055e41", "-t")

challkeys=[]
f=open("ChallengerDiv0609.txt", "r")
line=f.readline()
while(line):
    if(line.split('|')[0]!='None'):
        print(line.split('|'))  
        challkeys.append(line.split('|')[0])
    line=f.readline()
MatchDataTable(challkeys, "RGAPI-6014d53d-88ea-4390-a23a-8c96fe055e41")
"""
#print(GetMatchData("4423996367","RGAPI-4ee81316-3c0d-446f-8072-dae173fd2961"))
"""
[4339025922, [[100, 'Leblanc'], [100, 'XinZhao'], [100, 'Tristana'], [100, 'Bard'], [100, 'Aphelios'], [200, 'Trundle'], [200, 'Yuumi'], [200, 'Ezreal'], [200, 'Kalista'], [200, 'Syndra']], [[100, 'Fail'], [200, 'Win']]]
How To Get Match Data
1. Get Summoner Name that contians Summoner's Id
2. Get Summoner Id that contians Summoner's acc id
3. Get Summoner's encrypted account Id
4. Get Matchlist using account id
5. Get Match Info
"""
#AvdVLfFbT-wZJV2fPrX_uE6l2eZpuFjvKbN1622JMafmRcE
"""
res = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/AvdVLfFbT-wZJV2fPrX_uE6l2eZpuFjvKbN1622JMafmRcE"+'?api_key='+api_key
r=requests.get(res)
#print(r.json())
enc_acc_id=r.json()['accountId']

res = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/"+enc_acc_id+'?api_key='+api_key
r=requests.get(res)
print(r.json()['matches'][0])
res = "https://kr.api.riotgames.com/lol/match/v4/matches/"+str(r.json()['matches'][0]['gameId'])+'?api_key='+api_key
r=requests.get(res)
print(r.json())
"""
