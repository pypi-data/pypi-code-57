# Copyright 2020 Alberto Martín Mateos and Niloufar Shoeibi
# See LICENSE for details.

# Copyright 2019-2020 Alberto Martín Mateos & Niloufar Shoeibi for TWINPICS project
# See LICENSE for details.
# -*- coding: utf-8 -*-

import subprocess
import sys
import warnings
warnings.filterwarnings("ignore")
#---------------------------------------------------------------INSTALLATION---------------------------------------------------------#

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("networkx==2.2")
install("pandas")
install("numpy")
install ("urllib3")
install("requests")
install("matplotlib")
install("tweepy")
install("nltk")
install("textblob")
install("fastdtw")
##----------------------------------------------IMPORTS---------------------------------------------------------------------------#	
import json
import itertools
import ast
import copy
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import pandas as pd
import numpy as np
import urllib3
import re
import time
import networkx as nx
import requests
import matplotlib.pyplot as plt
import tweepy
from os import path
from datetime import timedelta
from datetime import datetime

#---------------------------------------------NLP-Part-------------------------------------------------------------------------------#
from textblob import TextBlob
import nltk
from nltk import RegexpTokenizer
# some small toolkits to download
nltk.download("wordnet")
nltk.download('brown')
nltk.download('punkt')


#----------------------------------------FUNCTIONS-----------------------------------------------------------------------------#

def load_file(df):
    df = pd.read_json(df)
    return df

def merge_dataframes(df1, df2):
    df_final = pd.merge(df1, df2, on = ["screen_name"])
    return df_final

#----------------------------------Structure for the graph-----------------------------------------#
def profile_connections (data_tweets):    
    screen_name = []
    screen_name_mention = []
    data = pd.DataFrame()
    data_tweets = data_tweets.rename(columns = {"created_at": "created_at_tw"})
    data_tweets = pd.concat([data_tweets.drop(['user'], axis=1), data_tweets['user'].apply(pd.Series)],
                            axis=1).drop_duplicates().reset_index(drop=True)
    if(data_tweets.empty == False):
        for i in range(len(data_tweets)):
            screen_name.append(data_tweets["screen_name"][i])
            if "@" in (data_tweets["text"][i]):
                split_text = data_tweets["text"][i].split()
                check = "@"
                screen_name_mention1 = [idx for idx in split_text if idx.lower().startswith(check.lower())]
                #Consider that @ is from a email or another words that is not the screen_name
                if not screen_name_mention1:
                    screen_name_mention.append(["Empty"])
                else:
                    if(data_tweets["text"][i].startswith('RT',0)):
                        screen_name_mention1 = re.sub("[\[\]\'\"!@?¿#$:….]", '',str(screen_name_mention1)).split(", ") 
                        screen_name_mention.append([screen_name_mention1[0]])                    
                    else:
                        screen_name_mention.append(re.sub("[\[\]\'\"!@?¿#$:….]", '',str(screen_name_mention1)).split(", "))
            else:
                screen_name_mention.append(["Empty"])
    data["screen_name"] = screen_name    
    data["screen_name_mention"] = screen_name_mention  
    #Agruping
    lst_col = "screen_name_mention"
    data = data[["screen_name","screen_name_mention"]]
	#Create new rows in case of a tweet has different mentions
    data_ext =pd.DataFrame({col:np.repeat(data[col].values, data[lst_col].str.len())for col in data.columns.difference(
        [lst_col])}).assign(**{lst_col:np.concatenate(data[lst_col].values)})[data.columns.tolist()]
    data1_ext = pd.DataFrame({'iteration' : data_ext.groupby(data_ext.columns.tolist(),as_index=False).size().sort_values(
                                                                        ascending = False)}).reset_index()
    return data1_ext

#--------------------------------------Graph building functions---------------------------

def building_node_list(df):

    node_list = pd.DataFrame()
    n = []
    for i in range(len(df)):
        n.append(df['screen_name'].iloc[i])
        n.append(df['screen_name_mention'].iloc[i])
    node_list['screen_name']= n
    node_list = node_list.drop_duplicates()
    node_list = node_list[node_list["screen_name"] !="Empty"].reset_index()
    return list(node_list["screen_name"])

def building_DiGraph(node_list, df):
    DiG = nx.DiGraph()
    DiG.add_nodes_from(node_list)
    for i in range(len(df)):
        if(df['screen_name_mention'].iloc[i] !="Empty"):
            DiG.add_edge(df['screen_name'].iloc[i],df['screen_name_mention'].iloc[i])
    return DiG


def self_loop_iteration_nodes(df):
    df_self_loop_iteration_nodes = pd.DataFrame()
    n = []
    self_loop_iteration = []
    for i in range(len(df)):
        if(df["screen_name"].iloc[i] ==df["screen_name_mention"].iloc[i]):
            n.append(df['screen_name'].iloc[i])
            self_loop_iteration.append(df["iteration"].iloc[i])            
        else:
            n.append(df['screen_name'].iloc[i])
            n.append(df['screen_name_mention'].iloc[i])
            self_loop_iteration.append(0)
            self_loop_iteration.append(0)
    df_self_loop_iteration_nodes['screen_name']= n
    df_self_loop_iteration_nodes['self_loop_iteration']= self_loop_iteration
    df = pd.DataFrame({'times': df_self_loop_iteration_nodes.groupby(["screen_name","self_loop_iteration"]).size().sort_values(
    ascending=False)}).reset_index().drop_duplicates(["screen_name"],keep="first")
    del df["times"]
    return df
	
def DiGraph_visualization (DiG):
    plt.figure(figsize=(30,18))
    nx.draw(DiG, with_labels=True, node_size=10, node_color="skyblue", node_shape="s", alpha=0.5, linewidths=4)
    plt.show()

#---------------------------------Graph features functions ----------------------
def in_degree_centrality(DiG, output):
    l = []
    l = nx.in_degree_centrality(DiG)
    sc = []
    indegcent = []
    for k, v in l.items():
        indegcent.append(v)
        sc.append(k)
    output['in_degree_centrality']=indegcent
    output["screen_name"] = sc    
    return output

def out_degree_centrality(DiG, output):
    l=[]
    l=nx.out_degree_centrality(DiG)
    sc=[]
    outd=[]
    for k, v in l.items():
        outd.append(v)
    output['outdegree_centrality']=outd
    return output

def degree_centrality(DiG,output):
    l=[]
    l=nx.degree_centrality(DiG)
    deg=[]
    for k, v in l.items():
        deg.append(v)
    output['degree_centrality']=deg
    return output

def in_degree(DiG, output):
    indegs=[]
    for i in range(len(list(DiG.nodes))):
        indegs.append(DiG.in_degree(list(DiG.nodes)[i]))
    output['in_degree']=indegs
    return output

def out_degree(DiG, output):
    outdegs=[]
    for i in range(len(list(DiG.nodes))):
        outdegs.append(DiG.out_degree(list(DiG.nodes)[i]))
    output['out_degree']=outdegs
    return output

def degree(DiG, output):
    degs=[]
    for i in range(len(list(DiG.nodes))):
        degs.append(DiG.degree(list(DiG.nodes)[i]))
    output['degree']=degs
    return output

def self_loops(DiG, output):
    SL = list(DiG.nodes_with_selfloops())
    output['self_loop']= False
    l=[]
    for i in range(len(SL)):
        for j in range(len(output)):
            if SL[i]==output['screen_name'].iloc[j]:
                output.self_loop.iloc[j]=True
    return output


def graph_features(DiG,df):

    output = pd.DataFrame()
    output = in_degree_centrality(DiG, output)
    output = out_degree_centrality(DiG, output)
    output = degree_centrality(DiG, output)
    output = in_degree(DiG, output)
    output = out_degree(DiG, output)
    output = degree(DiG, output)
    output = self_loops(DiG, output)
    df_nodes_self_loop_iteration = self_loop_iteration_nodes(df)
    output = merge_dataframes(output, df_nodes_self_loop_iteration)
    return output

def user_timeline_extraction(node_list, consumerKey, consumerSecret,accessToken,accessTokenSecret,filepath, filename,n_groups=1,save_by=300):
    # get_user Returns the 20 most recent statuses posted from the authenticating user or the user specified. 
    profile_iter = save_by
    k=0
    auth = tweepy.OAuthHandler(consumerKey[0], consumerSecret[0])
    auth.set_access_token(accessToken[0], accessTokenSecret[0])
    api = tweepy.API(auth)
    nc= 0
    ultima = 0
    origen1 = time.time()
    while ((k<= (len(node_list)+profile_iter)) & (ultima !=2) ):
      tweets_user=[]
      list_users_noInfo = []
      origen2 = time.time()
      i=0
      if ((len(node_list)>= k) & ((len(node_list)-profile_iter) <=k)):
        node_list1 = node_list[k:len(node_list)]
        ultima = 1
      else:
        node_list1 = node_list[k:k+profile_iter]
      while(i <(len(node_list1))):         
        pri = 0
        itera=0
        max_id=""
        intentos = 0
        while itera != n_groups:
          try:
            if pri ==0:
              user=api.user_timeline(node_list1[i], count=200,tweet_mode="extended")      
              tweets_user.append(user)
              max_id = str(tweets_user[len(tweets_user)-1][len(tweets_user[len(tweets_user)-1])-1]._json["id_str"])
              pri=1
              itera = itera+1
            else:
              user=api.user_timeline(node_list1[i], count=200,tweet_mode="extended", max_id=max_id)
              tweets_user.append(user)
              max_id = str(tweets_user[len(tweets_user)-1][len(tweets_user[len(tweets_user)-1])-1]._json["id_str"])
              itera = itera+1
              intentos=0 # Para si justo es el primero el que no se puede extraer y no es problema de agotar claves
          except:
            nc = nc+1
            n_clave = len(consumerKey)
            if(nc == n_clave):
              nc= 0
            auth = tweepy.OAuthHandler(consumerKey[nc], consumerSecret[nc])
            auth.set_access_token(accessToken[nc], accessTokenSecret[nc])
            api = tweepy.API(auth)
            intentos = intentos + 1
            if(intentos == 2):         
              list_users_noInfo.append(node_list1[i])
              intentos = 0
              itera=n_groups
        i = i+1       
      destino2 = time.time()
      aux=[]
      for i in range( len(tweets_user)):
        for j in range(len(tweets_user[i])):          
            aux.append(tweets_user[i][j]._json)     
      if(len(aux) != 0):  
        df = pd.DataFrame(aux)
        df = df.rename(columns = {"created_at": "created_at_tw"})
        df= df.rename(columns = {"lang": "lang_tw"})
        df = pd.concat([df.drop(['user'], axis=1), df['user'].apply(pd.Series)], axis=1)
        df = df.rename(columns={"followers_count": "followers",
                              "friends_count": "followees",
                              "retweet_count": "retweets",
                              "favorite_count": "favorites",
                              "favourites_count": "favorites_count",
                              "full_text": "text"})
        df2 = metadata_extraction(df)
        if path.exists(filepath + filename):
          df2.to_csv(filename,mode="a", index=False, header=False)
        else:
          df2.to_csv(filename,index=False)         
        if len(list_users_noInfo) !=0:
          nodes = pd.DataFrame()
          nodes["nodos"] = list_users_noInfo
          if path.exists(filepath+"node_without_"+filename):
            nodes.to_csv("node_without_"+ filename, mode ="a",index=False, header=False)          
          else:
             nodes.to_csv("node_without_"+ filename, index=False)
        k = k+profile_iter        
        if ultima ==1:          
          ultima =2
      else:
        print("Repetimos")
    print("Lista de usuarios sin metadata")
    print(list_users_noInfo)
    destino1 = time.time()
    return df2, list_users_noInfo

def separate_text_tweets_feature(df_metadata):
  df_metadata["RT_days_list"] = 0
  df_metadata["lang_days_list"] = 0
  for k in range(len(df_metadata)):
    data_tweets = df_metadata.iloc[k]["text_tweets_days_list"]
    text_tweets_day = []
    text_tweets_days = []
    lang_text_tweets_day = []
    lang_text_tweets_days = []
    RT_text_tweets_day = []
    RT_text_tweets_days = []
    for i in range(len(data_tweets)):
      text_tweets_day = []
      lang_text_tweets_day = []
      RT_text_tweets_day = []
      if (len(data_tweets) ==1) & (len(data_tweets[0])==3):
        try:
          text_tweets_days.append(data_tweets[i]["text"]+"¿¿??##%")
          lang_text_tweets_days.append(data_tweets[i]["lang"])
          RT_text_tweets_days.append(str(data_tweets[i]["RT"]))
        except:
          for j in range(len(data_tweets[i])):
            text_tweets_day.append(data_tweets[i][j]["text"]+"¿¿??##%")
            lang_text_tweets_day.append(data_tweets[i][j]["lang"])
            RT_text_tweets_day.append(str(data_tweets[i][j]["RT"]))
          text_tweets_days.append(text_tweets_day)
          lang_text_tweets_days.append(lang_text_tweets_day)
          RT_text_tweets_days.append(RT_text_tweets_day) 
      else:
        for j in range(len(data_tweets[i])):
          text_tweets_day.append(data_tweets[i][j]["text"]+"¿¿??##%")
          lang_text_tweets_day.append(data_tweets[i][j]["lang"])
          RT_text_tweets_day.append(str(data_tweets[i][j]["RT"]))
        text_tweets_days.append(text_tweets_day)
        lang_text_tweets_days.append(lang_text_tweets_day)
        RT_text_tweets_days.append(RT_text_tweets_day)
    df_metadata["text_tweets_days_list"].iloc[k] = text_tweets_days    
    df_metadata["lang_days_list"].iloc[k] = lang_text_tweets_days
    df_metadata["RT_days_list"].iloc[k]= RT_text_tweets_days
  return df_metadata
  
#----------------------------------Extract metadata-----------------------------------------------------------#
def metadata_extraction (df_users):
    
	users = df_users["screen_name"].unique()
	count_users=0
	df = pd.DataFrame() 
	for i in range(len(users)):
		data_tweets = df_users[df_users["screen_name"]==users[i]].reset_index()
		
		data = pd.DataFrame()              
		if(data_tweets.empty == False):       
			count_users = count_users + 1
			print("Usuarios: %f" % count_users)
			[screen_name_mention_user,seasonalityDF,tweets_urlDF,mentionsDF,text_tweetsDF,
			 fav_twDF_list,ret_twDF_list,fav_twDF,ret_twDF,RT_tw,ntwPro_DF,minu_tw,tw_per_days_list,
			 text_tweets_days_list,tweet_date_days_list,duplicated,minu_tw_answer,
			 tw_day_list] = text_tweets_features_extraction(data_tweets)
			data["screen_name_mention_user"] = screen_name_mention_user
			data["screen_name"] = data_tweets["screen_name"].iloc[0]  
			data["created_at"] = data_tweets["created_at"].iloc[0]
			data["following"] = data_tweets["followees"].iloc[0]
			data["followers"] = data_tweets["followers"].iloc[0]
			data["statuses_count"] = data_tweets["statuses_count"].iloc[0]
			data["default_profile"] = data_tweets["default_profile"].iloc[0]
			data["default_profile_image"] = data_tweets["default_profile_image"].iloc[0]
			data["biography_profile"] = data_tweets["description"].iloc[0]
			data["listed_count"] = data_tweets["listed_count"].iloc[0]    
			data["favourite_count"] = data_tweets["favorites_count"].iloc[0]
			data["seasonality"] = seasonalityDF    
			data["tweets_url"] = tweets_urlDF    
			data["mentions"] = mentionsDF 
			data["text_tweets_days_list"] = text_tweets_days_list
			data["tweet_date_days_list"] = tweet_date_days_list   
			data["text_tweets"] = text_tweetsDF
			data["favorite_tweets_list"] = fav_twDF_list
			data["retweet_tweets_list"] = ret_twDF_list
			data["favorite_tweets_count"] = fav_twDF
			data["retweet_tweets_count"] = ret_twDF
			data["RT"] = RT_tw
			data["num_ownTw"] = ntwPro_DF    
			data["time_btw_tw"] = minu_tw
			data["tw_day_list"] = tw_day_list
			data["tw_per_day_list"] = tw_per_days_list
			data["tw_duplicated"] = duplicated
			data["minu_tw_answer"] = minu_tw_answer
			data["profile_type"] = data_tweets["verified"].iloc[0]
			data["screen_name_mention_user"] = data["screen_name_mention_user"].astype(str)
			probably_fake = []
			for j in range(len(data)):
				if data["biography_profile"].any()==False:# Si se lee el dataframe
				#if len(data["biography_profile"][j]) == 0:# Si se hace la extraccion antes de guardar los datos
					data["biography_profile"][j] = 1
				else:
					data["biography_profile"][j] = 0
				if data["following"].iloc[j] == 2001:
					probably_fake.append(1)
				else:
					probably_fake.append(0)
			data["probably_fake"] = probably_fake
			df = df.append(data, ignore_index=True)
	df =df.loc[df.astype(str).drop_duplicates().index].reset_index()

	df = time_twitter_account(df)
	df = time_series_tw(df)
	df = separate_text_tweets_feature(df)
	return df



def text_tweets_features_extraction(data_tweets):
   
	seasonalityDF = []
	tweets_urlDF = []
	mentionsDF = []
	text_tweetsDF = []
	fav_twDF= []
	ret_twDF = []
	ret_twDF_list = []
	fav_twDF_list = []
	ntwPro_DF= []
	RT_tw = []
	minu_tw = []
	minu_tw_answer = []
	tw_duplicated = []
	duplicated = []
	tw_per_day_list= []
	screen_name_mention_user = []
	tweets = []
	tweets_url = 0
	num_tw_day = 1
	is_RT=0
	is_RT_list= []
	screen_name_mention = []
	RT = []
	retweet_list = []
	favorite_list = []
	mentions = 0
	time_btw_tw = []
	tw_answer = []
	num_tw_days = []
	text_duplicated = []
	tw_day_list = []
	text_tweets_day = []
	text_tweets_days = []
	text_tweets_days_list = []
	#Almacenar la fecha entera de los tweets para si hay que consultar las horas de ese dia
	tweet_date_day = []
	tweet_date_days = []
	tweet_date_days_list = []
	lang_text_tweet = list(data_tweets["lang_tw"])
	text_tweets_user= list(data_tweets["text"])
	favorites= list(data_tweets["favorites"])
	retweets = list(data_tweets["retweets"])
	tweets_date= pd.to_datetime(data_tweets["created_at_tw"])
	for j in range(len(text_tweets_user)): #Comprobamos cuantos tweets han sido escritos por el usuario 
		if(text_tweets_user[j].startswith('RT',0)):
			RT.append(text_tweets_user[j])
			is_RT = 1
		else:
			is_RT=0          
			#Tweets with url from users
			if "http" in text_tweets_user[j]:
				tweets_url = tweets_url + 1
			#Tweets with mentions from users
			if "@" in text_tweets_user[j]:
				mentions = mentions + 1                        
			else:
				#Time of the answer of a tweet(tw --> @)
				if(j!=(len(text_tweets_user)-1)):
					if ("@" in text_tweets_user[j+1]):
						tw_answer.append((tweets_date[j] - tweets_date[j+1]) / np.timedelta64(1,'m'))
				#Found duplicated tweets where the only change the photo  that the users publish
				text_sinHttp = " ".join(filter(lambda x:x[0:4]!='http', text_tweets_user[j].split()))
				text_sinMencion = " ".join(filter(lambda x:x[0]!='@', text_sinHttp.split()))
				text_duplicated.append(text_sinMencion)
			tweets.append({"text":text_tweets_user[j], "lang": lang_text_tweet[j], "RT": 0})
			retweet_list.append(int(retweets[j]))
			favorite_list.append(int(favorites[j]))
		is_RT_list.append(is_RT)                                
		if(j!=0):
			#Time between tweets (RT + propios)
			time_btw_tw.append((tweets_date[j-1] - tweets_date[j]) / np.timedelta64(1,'m'))
			#Found if tweets are the same day
			#Second condition if all the tweets are the same day          
			if((tweets_date[j-1].date() == tweets_date[j].date()) & (j!=(len(text_tweets_user)-1))):                            
				
				#Create a list with the tweets of a day
				text_tweets_day.append({"text": " ".join(filter(lambda x:x[0:4]!='http', text_tweets_user[j-1].split())),"lang": lang_text_tweet[j-1],"RT": is_RT_list[j-1]})
				text_tweets_day.append({"text": " ".join(filter(lambda x:x[0:4]!='http', text_tweets_user[j].split())),"lang": lang_text_tweet[j], "RT": is_RT_list[j]})              
				tweet_date_day.append(tweets_date[j-1])
				tweet_date_day.append(tweets_date[j])                         
			else:
				if(j==(len(text_tweets_user)-1)):                  
					if(tweets_date[j-1].date() == tweets_date[j].date()):                     
						text_tweets_day.append({"text": " ".join(filter(lambda x:x[0:4]!='http', text_tweets_user[j-1].split())),"lang": lang_text_tweet[j-1],"RT": is_RT_list[j-1]})
						text_tweets_day.append({"text": " ".join(filter(lambda x:x[0:4]!='http', text_tweets_user[j].split())),"lang": lang_text_tweet[j], "RT": is_RT_list[j]})           
						tweet_date_day.append(tweets_date[j-1])
						tweet_date_day.append(tweets_date[j])
						                     
						text_tweets_days.append([i for n, i in enumerate(text_tweets_day) if i not in text_tweets_day[n + 1:]] )
						tweet_date_days.append(list(dict.fromkeys(tweet_date_day)))
						num_tw_days.append(len(list(dict.fromkeys(tweet_date_day))))
						num_tw_day = 1 
						text_tweets_day = []
						tweet_date_day = []
					else:                      
						text_tweets_day.append({"text": " ".join(filter(lambda x:x[0:4]!='http', text_tweets_user[j-1].split())),"lang": lang_text_tweet[j-1],"RT": is_RT_list[j-1]})				                                   
						tweet_date_day.append(tweets_date[j-1]) 
						num_tw_days.append(1)                     
						text_tweets_days.append([i for n, i in enumerate(text_tweets_day) if i not in text_tweets_day[n + 1:]])
						tweet_date_days.append(list(dict.fromkeys(tweet_date_day)))
						text_tweets_day = []
						tweet_date_day = []                      
						tweet_date_day.append(tweets_date[j])                     
						text_tweets_day.append({"text": " ".join(filter(lambda x:x[0:4]!='http', text_tweets_user[j].split())),"lang": lang_text_tweet[j], "RT": is_RT_list[j]})              
						num_tw_days.append(1)
						text_tweets_days.append([i for n, i in enumerate(text_tweets_day) if i not in text_tweets_day[n + 1:]] )
						tweet_date_days.append(list(dict.fromkeys(tweet_date_day)))
						num_tw_day = 1 
						text_tweets_day = []
						tweet_date_day = []                      
				else:
					if(num_tw_day ==1):
						text_tweets_day.append({"text": " ".join(filter(lambda x:x[0:4]!='http', text_tweets_user[j-1].split())),"lang": lang_text_tweet[j-1],"RT": is_RT_list[j-1]})	
						tweet_date_day.append(tweets_date[j-1])                  
					text_tweets_days.append([i for n, i in enumerate(text_tweets_day) if i not in text_tweets_day[n + 1:]] )
					tweet_date_days.append(list(dict.fromkeys(tweet_date_day)))
					num_tw_days.append(len(list(dict.fromkeys(tweet_date_day))))
					num_tw_day = 1 
					text_tweets_day = []
					tweet_date_day = []
		if "@" in (text_tweets_user[j]):
			split_text = text_tweets_user[j].split()
			check = "@"
			screen_name_mention1 = [idx for idx in split_text if idx.lower().startswith(check.lower())] 
			if not screen_name_mention1:
				screen_name_mention.append(["Empty"])
			else:
				screen_name_mention1 = re.sub("[\[\]\'\"!@?¿#$:….,]", '',str(screen_name_mention1)).split(", ")
				if(text_tweets_user[j].startswith('RT',0)):
					screen_name_mention.append([screen_name_mention1[0]])                    
				else:
					screen_name_mention.append(screen_name_mention1)
		else:
			screen_name_mention.append(["Empty"])

	if(len(set(text_duplicated)) != len((text_duplicated))):
		duplicated.append(len(text_duplicated) - len(set(text_duplicated)))
	else:
		duplicated.append(0)
    
	#Maximun tweets for user
	if not num_tw_days:
		text_tweets_days_list.append([{"text":"Empty", "lang":"und","RT":2}])
		tweet_date_days_list.append(["Empty"])
		tw_per_day_list.append([0])
	else:
		text_tweets_days_list.append(text_tweets_days)
		tweet_date_days_list.append(tweet_date_days)
		tw_per_day_list.append(num_tw_days)

	tw_day_list.append(list(sorted(set(tweets_date.dt.date), reverse=True)))
	screen_name_mention_user.append(screen_name_mention)
	seasonalityDF.append(np.std(time_btw_tw))
	tweets_urlDF.append(tweets_url)
	mentionsDF.append(mentions)
	text_tweetsDF.append(tweets)
	fav_twDF_list.append(favorite_list)
	ret_twDF_list.append(retweet_list)
	fav_twDF.append(int(sum(favorite_list)))
	ret_twDF.append(int(sum(retweet_list)))
	ntwPro_DF.append(int(len(tweets)))
	RT_tw.append(int(len(RT)))
	minu_tw.append(int(sum(time_btw_tw)))
	#Time between tweets and its answer
	if not tw_answer:
		minu_tw_answer.append(0)
	else:   
		minu_tw_answer.append(int(sum(tw_answer))/len(tw_answer))
        
	return [screen_name_mention_user,seasonalityDF,tweets_urlDF,mentionsDF,text_tweetsDF,
			fav_twDF_list,ret_twDF_list,fav_twDF,ret_twDF,RT_tw,ntwPro_DF,minu_tw,tw_per_day_list,
			text_tweets_days_list,tweet_date_days_list,duplicated,minu_tw_answer,tw_day_list]

def time_twitter_account(df):

    anio_actual = time.strftime("%Y")
    df["creation_day"] = 0
    df["twitter_years"] = 0
    for i in range(len(df)):
        df["creation_day"][i] = df.iloc[i]["created_at"].split(' ')[-1]
        df["twitter_years"][i] = int(anio_actual) - int(df['creation_day'][i]) + 1
    return df

def time_series_tw (df):
    for index, row in df.iterrows():
        restart=True
        while restart == True:
            restart=False
            for k in range(len(df.loc[index, "tw_day_list"])-1):
                if(int((df.loc[index, "tw_day_list"][k] - df.loc[index,"tw_day_list"][k+1]).days))>1:
                    times = int((df.loc[index, "tw_day_list"][k] - df.loc[index,"tw_day_list"][k+1]).days)
                    for j in range(times-1):
                        df.loc[index,"tw_per_day_list"].insert(k+1,0)
                        df.loc[index, "tweet_date_days_list"].insert(k+1,["Empty"])
                        df.loc[index,"text_tweets_days_list"].insert(k+1, [{"text":"Empty","lang": "und","RT":2}])
                        df.loc[index, "tw_day_list"].insert(k+j+1, (df.loc[index,"tw_day_list"][k] - timedelta(days=j+1)))
                    restart = True
    return df 

#-------------------------------------------Ratios and other advanced features----------------------------------#
def duplicates_detection(data, i):
    num_duplicates_tweets = []
    if i < len(data):
        possible_duplicated = []
        for j in range(len(data)):
            if j !=i:
                list_dtw_1 = np.array(data["tw_per_day_list"].iloc[i])              
                list_dtw_2 = np.array(data["tw_per_day_list"].iloc[j])
                distance, path = fastdtw(list_dtw_1,list_dtw_2)
                if (distance < 600):
                    possible_duplicated.append({"screen_name":data["screen_name"].iloc[j], "distance": distance})
        if (len(possible_duplicated)==0):
            possible_duplicated.append({"screen_name": "Empty", "distance": "Empty"})           
        data["possible_duplicates"].iloc[i] = possible_duplicated
        if (data["possible_duplicates"].iloc[i][0]["screen_name"] =="Empty"):
            num_duplicates_tweets.append(0)
        else:          
            for t in range(len(data["possible_duplicates"].iloc[i])):
                #text_1 is the differences possible duplicates with the profile evaluate
                text_1_aux = pd.DataFrame({"text":data[data["screen_name"] == data["possible_duplicates"].iloc[i][t]["screen_name"]]["text_tweets_days_list"]})
                text_1 = pd.DataFrame()
                for a in range(len(text_1_aux)):
                    aux2 = pd.DataFrame({'text':text_1_aux["text"].iloc[a]})
                    text_1 = text_1.append(aux2, ignore_index=False).reset_index(drop=True)
                text_1 = list(itertools.chain(*text_1["text"]))                
                text_2 = list(itertools.chain(*data.iloc[i]["text_tweets_days_list"]))
                if "Empty" in text_1:
                  text_1 = list(filter(("Empty").__ne__, text_1))
                if "Empty" in text_2:  
                  text_2 = list(filter(("Empty").__ne__, text_2))
                comparacion = [item for item in text_1 if item in text_2]
                if len(comparacion) > 0:
                    data["possible_duplicates"].iloc[i][t]["tw_similarity"] = len(comparacion)/(data["num_userTw"].iloc[i])
                else:
                    data["possible_duplicates"].iloc[i][t]["tw_similarity"] = 0
    return data
	
def advanced_features(data):
    
    #Posible bot
    data["screen_name_bot"] = 0 
    data["days_with_tw"] = 0
    data["max_fav_tw"] = 0
    data["max_ret_tw"] = 0
    data["follow_rate"] = 0
    data["max_tw_day"] = 0
    data["index_max_day_tw"]=0
    data["num_duplicates_list"] = 0
    data["possible_duplicates"] = 0

    data["num_userTw"]= data["num_ownTw"] + data["RT"]
    data["tw_RT_rate"] = ((((data["num_ownTw"]))) / (data["num_userTw"])).replace([np.inf, -np.inf], np.nan).fillna(0)
    data["sum_fav_RT_ownTw"] = (data["retweet_tweets_count"] + data["favorite_tweets_count"]).replace([np.inf, -np.inf], np.nan).fillna(0)
    data["iter_fav_RT_rate"] = (data["sum_fav_RT_ownTw"] / data["num_ownTw"]).replace([np.inf, -np.inf], np.nan).fillna(0)
    data["tw_year_rate"] = ((data["statuses_count"]) / (data["twitter_years"])).replace([np.inf, -np.inf], np.nan).fillna(0)
    data["time_tw_rate"] = (data["time_btw_tw"] / data["num_userTw"]).replace([np.inf, -np.inf], np.nan).fillna(0)
    data["seasonality"] = data["seasonality"].replace([np.inf, -np.inf], np.nan).fillna(0)
    data["fake_sum"] = data["default_profile_image"] + data["biography_profile"]+ data["screen_name_bot"]
    data["fake_rate"] = ((data["tweets_url"] + data["mentions"]) /data["num_ownTw"]).replace([np.inf, -np.inf], np.nan).fillna(0)
    data["follow_rate"][data["followers"]== 0] = np.median(data["follow_rate"])
    num_duplicates_tweets_list = []
    for i in range(len(data)):
        if (len(str(data.iloc[i]["screen_name"])) > 4):
            if((data.iloc[i]["screen_name"][-1].isdigit()) & (data.iloc[i]["screen_name"][-2].isdigit()) & 
                (data.iloc[i]["screen_name"][-3].isdigit()) &(data.iloc[i]["screen_name"][-4].isdigit())):
                data["screen_name_bot"].iloc[i] = 1
        else:
            data["screen_name_bot"].iloc[i] = 1   

        if(data.iloc[i]["following"]== 0):
            data["follow_rate"].iloc[i] = 0
        else:
            data["follow_rate"].iloc[i] = (data.iloc[i]["following"] / data.iloc[i]["followers"])
        
        #ast.literal_eval cuando se leen los datos del csv porque no recoge bien la lista de valores
        #Favorites and Retweets in their published tweets
        if not ((data["favorite_tweets_list"].iloc[i])):
            data["max_fav_tw"].iloc[i] = 0
        else:
            data["max_fav_tw"].iloc[i] = max((data["favorite_tweets_list"].iloc[i]))
        
        if not ((data["retweet_tweets_list"].iloc[i])):
            data["max_ret_tw"].iloc[i] = 0
        else:
            data["max_ret_tw"].iloc[i] = max((data["retweet_tweets_list"].iloc[i]))
          
        data = duplicates_detection(data, i)
        data["max_tw_day"].iloc[i] =max((data["tw_per_day_list"].iloc[i]))
        data["days_with_tw"].iloc[i] = len(data["tw_per_day_list"].iloc[i])
        data["index_max_day_tw"].iloc[i] = data["tw_per_day_list"].iloc[i].index(data["max_tw_day"].iloc[i])        
    data = trend_tweets_features(data) 
        
    return data
	
def trend_tweets_features(data):
    data["num_anom"] = 0
    data["trend"] = 0
    data["anom_rate"] = 0
    for i in range(len(data)):
        #trend rates
        if len(data.iloc[i]["tw_per_day_list"]) >4:
			#Select 95% confidence interval of a normal distribution to say that a values of tweet per day is an outlier
            df_aux= pd.DataFrame(data.iloc[i]["tw_per_day_list"])
            df_aux["floor"] = df_aux[0].mean() - 1.64 * df_aux[0].std()
            df_aux["roof"] = df_aux[0].mean() + 1.64 * df_aux[0].std() 
			#
            df_aux["anom"] = df_aux.apply(lambda row: row[0] if (row[0]<= row["floor"] or 
                                                                 row[0]>= row["roof"]) else 0, axis =1) 
            data["num_anom"].iloc[i] = len(list(filter(lambda x: x != 0, df_aux["anom"])))
            data["anom_rate"].iloc[i] = data["num_anom"].iloc[i] / len(data["tw_per_day_list"].iloc[i])
            if (data["num_anom"].iloc[i] ==1):
                if max(df_aux["anom"])== data["max_tw_day"].iloc[i]:
                    data["trend"].iloc[i] = 0
                else:
                    data["trend"].iloc[i]=1                    
            else:
                if data["max_tw_day"].iloc[i] in list(filter(lambda x: x != 0, df_aux["anom"])):                    
                    data["trend"].iloc[i] = 0
                else:
                    data["trend"].iloc[i]=1  
        else:
            data["trend"].iloc[i] =2 
            data["num_anom"].iloc[i] =0
            data["anom_rate"].iloc[i]=0
    return data
	
def text_to_list_features_conversor (data):
	for index, row in data.iterrows():
		data["favorite_tweets_list"].iloc[index] = ast.literal_eval(data.loc[index, "favorite_tweets_list"])
		data["retweet_tweets_list"].iloc[index] = ast.literal_eval(data.loc[index,"retweet_tweets_list"])
		data["tw_per_day_list"].iloc[index] = ast.literal_eval(data.loc[index,"tw_per_day_list"])
		data["text_tweets_days_list"].iloc[index] = data.loc[index,"text_tweets_days_list"].replace('"', "'").replace("], [","?#??").strip("[]'").split("?#??")
		list_day = []                                                                                
		list_text_tweets_day = []
		list_tweet_date_days = []
		list_RT_days = []
		list_lang_days = []
		text_days = data.loc[index,"tw_day_list"].strip("][").replace(")", ")??").split("??, ")
		tweet_date_days = data.loc[index,"tweet_date_days_list"].replace("], [","???").split("???")
		RT_days = data.loc[index, "RT_days_list"].strip("[]").split("], [")
		lang_days = data.loc[index, "lang_days_list"].strip("[]").split("], [")
		for i in range(len(text_days)):
			tweet_date_day = tweet_date_days[i].replace("), ",")??").strip("[]").split("??")
			text_tweets_day = data["text_tweets_days_list"].iloc[index][i].replace('"', "'").replace("¿¿??##%', '","¿¿??##%").strip("[]'").split("¿¿??##%")[:-1]
			RT_day = list(ast.literal_eval(str(RT_days[i])))
			if len(lang_days[i])<6:
				lang_day = [lang_days[i]]
			else:
				lang_day = list(ast.literal_eval(lang_days[i]))
			list_tweet_date_day = []
			for j in range(len(tweet_date_day)):                
				if(tweet_date_day == ["'Empty'"]):
					list_tweet_date_day.append("Empty")
				else:
					list_tweet_date_day.append(datetime.strptime(tweet_date_day[j],"Timestamp('%Y-%m-%d %H:%M:%S%z', tz='UTC')"))    
			if i == len(text_days)-1:
				text_days[i] = text_days[i].replace("??","")
			list_day.append(datetime.strptime(text_days[i],'datetime.date(%Y, %m, %d)' ).date())
			list_text_tweets_day.append(text_tweets_day)
			list_tweet_date_days.append(list_tweet_date_day)
			list_RT_days.append(RT_day)
			list_lang_days.append(lang_day)
		data["text_tweets_days_list"].iloc[index] = list_text_tweets_day
		data["tw_day_list"].iloc[index]= list_day
		data["tweet_date_days_list"].iloc[index]= list_tweet_date_days
		data["RT_days_list"].iloc[index] = list_RT_days
		data["lang_days_list"].iloc[index] = list_lang_days
	return data
	

#----------------------------------------------Filters-------------------------------------------------------#



def abnormal_categories_profiles(data_join):
    data_join["evaluate_NLP"] ="No"   
    
    
    #1.Profiles old spreader
    data_join["evaluate_NLP"][(data_join["index_max_day_tw"] >=30) & (data_join["profile_type"]==False) &
                  (data_join["max_tw_day"]>60)] ="NLP-F0"  
    
    #2.Profiles with low number of tweets but with a high iteration
    data_join["evaluate_NLP"][(data_join["trend"] == 0) & (data_join["profile_type"]==False) &
                  (data_join["max_tw_day"]<40) & (data_join["tw_RT_rate"]<0.2) &
                 ((data_join["max_ret_tw"]>500) | (data_join["max_fav_tw"]>500))] ="NLP-F1"
    
    #3.Profiles with a high number of RT in a specific day (try to spread information)
    data_join["evaluate_NLP"][(data_join["trend"] == 0) & (data_join["profile_type"]==False) &
                  (data_join["max_tw_day"]>150) & (data_join["tw_RT_rate"]<0.1) & 
                (data_join["evaluate_NLP"]=="No")] = "NLP-F2"
    
    #4.Possible influencer profile
    data_join["evaluate_NLP"][(data_join["trend"]==1) & (data_join["profile_type"]==False) &
             (data_join["in_degree"]>=5) & (data_join["followers"]>=3000) &
             (data_join["evaluate_NLP"]=="No")] = "NLP-F3"
    
    #5.Possible constant spreader
    data_join["evaluate_NLP"][(data_join["trend"]==1) & (data_join["profile_type"]==False) &
             (data_join["out_degree"]>=2) & (data_join["following"]>=3000) & (data_join["evaluate_NLP"]=="No")] = "NLP-F4"                

    #6.Possible new account with a high activity last days
    data_join["evaluate_NLP"][(data_join["trend"]==2) & (data_join["profile_type"]==False) &
             (data_join["twitter_years"]==1) & (data_join["max_tw_day"]>180) &
              (data_join["evaluate_NLP"]=="No")] = "NLP-F5"                     

    #7.Possible fake behaviour profile in the last days
    data_join["evaluate_NLP"][(data_join["trend"]==2) & (data_join["profile_type"]==False) &
             (data_join["fake_sum"]>=2) & (data_join["evaluate_NLP"]=="No")] = "NLP-F6" 
    
    #8.Possible influencers profile in the last days with a high iteration
    data_join["evaluate_NLP"][(data_join["trend"]==2) & (data_join["profile_type"]==False) &
             ((data_join["max_ret_tw"]>500) | (data_join["max_fav_tw"]>500)) &
                  (data_join["max_tw_day"]>210) &  (data_join["evaluate_NLP"]=="No")] = "NLP-F7"
    
    #9.Profiles BOT (more than tweet or RT each 5 minutes the 24 hours)
    data_join["evaluate_NLP"][(data_join["max_tw_day"]>	288) &(data_join["profile_type"]==False) &
                             (data_join["evaluate_NLP"]=="No")] ="NLP-8"
							 
    #10. More data required
    data_join["evaluate_NLP"][(data_join["trend"]==2) & (data_join["profile_type"]==False) & 
                              (data_join["max_tw_day"]>180) & (data_join["evaluate_NLP"]=="No")] = "More Data"

    return data_join


	
def more_tweets_required(df,df_graph_features,consumerKey,consumerSecret,accessToken,accessTokenSecret,filepath,filename,n_groups,save_by):
	df_evaluate = df[(df["evaluate_NLP"] !="No") & (df["evaluate_NLP"] !="More Data")]
	node_list_moreData = list(df[df["evaluate_NLP"]=="More Data"]["screen_name"])
	if len(node_list_moreData) >0:
		df_metadata_moreData, list_more_Data_noData = user_timeline_extraction(node_list_moreData,consumerKey,consumerSecret,accessToken,accessTokenSecret,filepath, filename,n_groups,save_by)
		df_metadata_moreData = pd.read_csv(filepath + filename)
		df_metadata_moreData = text_to_list_features_conversor(df_metadata_moreData)
		df_metadata_moreData = advanced_features(df_metadata_moreData)
		df_metadata_moreData = merge_dataframes(df_metadata_moreData,df_graph_features)
		df_metadata_moreData = abnormal_categories_profiles(df_metadata_moreData)
		df_metadata_moreData = df_metadata_moreData[(df_metadata_moreData["evaluate_NLP"] !="No") & (df_metadata_moreData["evaluate_NLP"] !="More Data")]
		df_evaluate = df_evaluate.append(df_metadata_moreData, ignore_index=True)
	return df_evaluate
	


def contextual_analysis_profile(data, keyword_corpus, hashtag_corpus):  
    #To remember which name of t he tw_per_day_list belongs each tweets
    n_list_tw = range(0, len(data["tw_per_day_list"]))
    aux = pd.DataFrame({'text':data["text_tweets_days_list"],'RT':data["RT_days_list"],'lang': data["lang_days_list"], 'n_list_tw':n_list_tw})
    tweets_df = pd.DataFrame()
    for i in range(len(aux)):
      aux2 = pd.DataFrame({'text':aux["text"].iloc[i],'RT':aux["RT"].iloc[i],'lang': aux["lang"].iloc[i],"n_list_tw": aux["n_list_tw"].iloc[i]})
      tweets_df = tweets_df.append(aux2, ignore_index=False).reset_index(drop=True)
    print(tweets_df)
    tweets_df = tweets_df[tweets_df["RT"] !="2"].reset_index(drop=True)
    tweets_df = sentiental_analysis_features(tweets_df)
    sample_data_tokenized = tokenize_tweets(tweets_df)
    tweets_df = keyword_score(tweets_df, sample_data_tokenized,keyword_corpus)
    tweets_df = hashtag_score(tweets_df,hashtag_corpus)	
    tweets_df["terrorist_suggestion"] = 0
    tweets_df["terrorist_suggestion"][(tweets_df["hashtag_score"]>0) | (tweets_df["keyword_score"]>0.2)] = 1
    tweets_irr_words = len(tweets_df[tweets_df["terrorist_suggestion"]==1])
    if len(tweets_df[tweets_df["terrorist_suggestion"]==1]) == 0:
      data["per_hash_key"] = 0
      data["negative_opinion"] = 0
      data["negative_fact"] = 0
      data["neutral"] = 0
      data["positive_fact"] = 0
      data["positive_opinion"] = 0
    else:
      data["per_hash_key"] = (len(tweets_df[tweets_df["terrorist_suggestion"]==1]) / len(tweets_df))
      tweets_df["terrorist_suggestion"][(tweets_df["terrorist_suggestion"]==1) & (tweets_df["polarity"] <= -0.1) & (tweets_df["subjectivity"]>=0.6)]= 2
      tweets_df["terrorist_suggestion"][(tweets_df["terrorist_suggestion"]==1) & (tweets_df["polarity"] <= -0.1) & (tweets_df["subjectivity"]<0.6)]= 3
      tweets_df["terrorist_suggestion"][(tweets_df["terrorist_suggestion"]==1) & (tweets_df["polarity"] < 0.1) & (tweets_df["polarity"] > -0.1)]= 4
      tweets_df["terrorist_suggestion"][(tweets_df["terrorist_suggestion"]==1) & (tweets_df["polarity"] >= 0.1) & (tweets_df["subjectivity"]<0.6)]= 5
      tweets_df["terrorist_suggestion"][(tweets_df["terrorist_suggestion"]==1) & (tweets_df["polarity"] >= 0.1) & (tweets_df["subjectivity"]>=0.6)]= 6
      if len(tweets_df[tweets_df["terrorist_suggestion"]==2]) == 0:
        data["negative_opinion"] = 0
      else:
        data["negative_opinion"] = (len(tweets_df[tweets_df["terrorist_suggestion"]==2]) / tweets_irr_words)
      if len(tweets_df[tweets_df["terrorist_suggestion"]==3]) == 0:
        data["negative_fact"] = 0
      else:
        data["negative_fact"] = (len(tweets_df[tweets_df["terrorist_suggestion"]==3]) / tweets_irr_words)
      if len(tweets_df[tweets_df["terrorist_suggestion"]==4]) == 0:
        data["neutral"] = 0
      else:
        data["neutral"] = (len(tweets_df[tweets_df["terrorist_suggestion"]==4]) / tweets_irr_words)
      if len(tweets_df[tweets_df["terrorist_suggestion"]==5]) == 0:
        data["positive_fact"] = 0
      else:
        data["positive_fact"] = (len(tweets_df[tweets_df["terrorist_suggestion"]==5]) / tweets_irr_words)
      if len(tweets_df[tweets_df["terrorist_suggestion"]==6]) == 0:
        data["positive_opinion"] = 0
      else:
        data["positive_opinion"] = (len(tweets_df[tweets_df["terrorist_suggestion"]==6]) / tweets_irr_words)
      
      tw_per_day_list_terrtw=[]
      for i in range(len(data["tw_per_day_list"])):
        tw_per_day_list_terrtw.append(len((tweets_df[(tweets_df["terrorist_suggestion"] !=0) & (tweets_df["n_list_tw"]==i)])))
      data["tw_per_day_list_terrTw"] = tw_per_day_list_terrtw
    return data,tweets_df

	
def contextual_analysis_profiles(data,keyword_corpus, hashtag_corpus):	
	final_df= pd.DataFrame()
	for i in range(len(data)):
		profile_evaluated, tweets_df = contextual_analysis_profile(data.iloc[i], keyword_corpus, hashtag_corpus)
		final_df = final_df.append(profile_evaluated, ignore_index=True)
	return final_df
	
def profile_trend_visualization(data, index):
	time_likes = pd.Series(data=data, index=index)
	time_likes.plot(figsize=(20, 8), color='r')
	plt.title('Daily Trend of Tweets',fontsize=20)
	plt.xlabel('Date',fontsize=15)
	plt.ylabel('Number of tweets',fontsize=15)
	plt.show()

def profile_max_tw_day_hourly_visualization(data):
	data["tweet_date_days_list_copy"] = copy.deepcopy(data["tweet_date_days_list"])
	date_list =data['tweet_date_days_list_copy'][data["index_max_day_tw"]]
	for i in range(len(date_list)):
		date_list[i] = date_list[i].time().hour    
	x = list(range(0,24))
	y = []
	for i in range(len(x)):
		count=0
		for j in range(len(date_list)):        
			if date_list[j] == i:
				count = count + 1
		y.append(count)
	del data["tweet_date_days_list_copy"]
	plt.title('Hourly Trend of Tweets around Max. Tweets',fontsize=20)
	plt.xlabel('Hour of the day',fontsize=15)
	plt.ylabel('Number of tweets',fontsize=15)
	plt.axis([0,23,0, max(y)+5])
	plt.locator_params(axis='x', nbins=24)
	plt.rcParams['figure.figsize'] = [10, 8]
	plt.plot(x,y)

	
def sentiental_analysis_features(data):
	corpus =[]
	polarities=[]
	subjectivities=[]
	for tweet in data.text:
		corpus.append(TextBlob(tweet.lower()))
	for i in range(len(corpus)):
		polarities.append(corpus[i].polarity)
		subjectivities.append(corpus[i].subjectivity)
	data['polarity']= polarities
	data['subjectivity']= subjectivities
	return data

def distribution_sentiment_tweets(data):
	### VISUALIZATION
	plt.rcParams['figure.figsize'] = [40, 20]
	for i in range (len(data)):
		x=data.polarity.iloc[i]
		y=data.subjectivity.iloc[i]
		if x>0.1 : # blue   red
			if y>0.5:  # yellow   green
				plt.scatter(x,y, color='blue')
			else: 
				plt.scatter(x,y, color='pink')
		elif -0.1<=x<=0.1:
			plt.scatter(x,y, color='gold')
		else:
			if y>0.5:  # yellow   green
				plt.scatter(x,y, color='purple')
			else: 
				plt.scatter(x,y, color='red')  
	plt.text(x+0.01, y+0.01, 'tweet'+str(i), fontsize=10)
	plt.xlim(-1,1)
	plt.ylim(0,1)
	plt.title('Scatter plot of sentiment analysis',fontsize=20)
	plt.xlabel('<------------------ NEGATIVE ------------------   POLARITY ------------------ POSITIVE ------------------>',fontsize=15)
	plt.ylabel('<----------------- FACTS ------------------ SUBJECTIVITY ------------------ OPINIONS ----------------->',fontsize=15)
	plt.show()

def general_pieChart(data):
	plt.rcParams['figure.figsize'] = [9, 6]	
	p=0 # positive
	n=0 # Negative
	o=0 # neutral
	for i in range(len(data)):
		if data['polarity'].iloc[i]>0.1:
			p+=1
		elif data['polarity'].iloc[i]<-0.1:
			n+=1
		else:
			o+=1
	f=0
	op=0
	kn=0
	for i in range(len(data)):
	  if data['subjectivity'].iloc[i]>0.5:
		  op+=1
	  else:
		  f+=1
	plt.rcParams['figure.figsize'] = [10,5]
	labels = 'Positive', 'Negative','Neutral'
	sizes = [p,n,o]
	colors = ['blue','red', 'gold'] #, 'yellowgreen', 'lightcoral','lightskyblue',
	explode = (0, 0,0)  # explode 1st slice

	labels2='Opinion','Fact'
	sizes2=[f,op]
	colors2=['pink','red']
	explode2=(0,0)

	fig, (ax1, ax2) = plt.subplots(1, 2)
	# Plot
	ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
	ax2.pie(sizes2, explode=explode2, labels=labels2, colors=colors2, autopct='%1.1f%%', shadow=True, startangle=140)
	plt.title('The General Sentiment Analysis of all The tweets')
	plt.axis('equal')
	plt.show()
	

	
def tokenize_tweets(data):
	sample_data_tokenized=[]  
	tokenizer=RegexpTokenizer(r'\w+')
	for tweets in data.text:
		sample_data_tokenized.append(tokenizer.tokenize(tweets.lower()))
	return sample_data_tokenized
	
def define_hashtags(data):
	hashtags=[]
	for i in range(len(data)):
		h= (re.findall(r"#(\w+)", data.text.iloc[i]))
		t=[]
		for i in range(len(h)):
			t.append('#'+h[i].lower())
		hashtags.append(t)
	data['hashtags']=hashtags
	return data
	
def keyword_score(data,sample_data_tokenized, keyword_corpus):
	scores = []
	for i in range(len(sample_data_tokenized)):
		score=0
		for c in keyword_corpus.keywords:
			for t in sample_data_tokenized[i]:
				if c==t:
					score+=1
		try:
			scores.append(score/len(sample_data_tokenized[i]))
		except ZeroDivisionError:
			scores.append(0)
	data['keyword_score']=scores
	return data


def hashtag_score(data, hashtags_corpus):
	scores=[]
	data = define_hashtags(data)
	for hshtgs in data.hashtags:
		score = 0
		for h in hshtgs:
			#print(h)
			for H in hashtags_corpus.hashtags:
				if h == H:
					score += 1
		scores.append(score)
	data['hashtag_score'] = scores
	data['index'] = [i for i in range(len(data))]
	data['names']= ['TWEET '+str(i) for i in range(len(data))]
	return data
	
def terrorist_keywords_belonging(data):
	temp = data[data['keyword_score']>0.2].reset_index(drop=True)
	# Draw plot
	fig, ax = plt.subplots(figsize=(36,8), dpi= 80)
	ax.vlines(x=temp.index, ymin=0, ymax=temp.keyword_score, color='firebrick', alpha=0.7, linewidth=2)
	ax.scatter(x=temp.index, y=temp.keyword_score, s=75, color='firebrick', alpha=0.7)
	# Title, Label, Ticks and Ylim
	ax.set_title('Terrorist Corpus Belonging Score of the Tweets', fontdict={'size':22})
	ax.set_ylabel('Belonging Score of each tweet to the cluster' )
	ax.set_ylabel('Tweets')
	ax.set_xticks(temp.index)
	ax.set_xticklabels(temp.names.str.upper(), rotation=90, fontdict={'horizontalalignment': 'right', 'size':12})
	ax.set_ylim(0, 1)
	# Annotate
	for row in temp.itertuples():
		ax.text(row.Index, row.keyword_score+0.15,rotation=90, s=round(row.keyword_score, 2), horizontalalignment= 'center', verticalalignment='bottom', fontsize=14)
	plt.show()
	
def pie_chart_keywords_terrorist(data):
	plt.rcParams['figure.figsize'] = [9, 6]
	data_terr = data[data['keyword_score']>0.2].reset_index(drop=True)
	p=0
	n=0
	o=0
	for i in range(len(data_terr)):
		if data_terr['polarity'].iloc[i]>0.1:
			p+=1
		elif data_terr['polarity'].iloc[i]<-0.1:
			n+=1
		else:
			o+=1
	f=0
	op=0
	for i in range(len(data_terr)):
		if data_terr['subjectivity'].iloc[i]>0.5:
			op+=1
		else:
			f+=1
	labels = 'Positive', 'Negative','Neutral'
	sizes = [p,n,o]
	colors = ['yellowgreen','red', 'gold'] #, 'yellowgreen', 'lightcoral','lightskyblue',
	explode = (0, 0,0)  # explode 1st slice
	labels2='Opinion','Fact'
	sizes2=[f,op]
	colors2=['lightblue','yellow']
	explode2=(0,0)
	fig, (ax1, ax2) = plt.subplots(1, 2)
	# Plot
	ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
	ax2.pie(sizes2, explode=explode2, labels=labels2, colors=colors2, autopct='%1.1f%%', shadow=True, startangle=140)
	plt.title('From '+str(len(data))+' tweets, '+ str(len(data_terr))+' are having Terrorist Corpus Score ')
	plt.axis('equal')
	plt.show()
	

def terrorist_hashtags_belonging(data):
	temp = data[ data['hashtag_score']>0].reset_index(drop=True)
	# Draw plot
	fig, ax = plt.subplots(figsize=(24,8), dpi= 80)
	ax.vlines(x=temp.index, ymin=0, ymax=temp.hashtag_score, color='firebrick', alpha=0.7, linewidth=2)
	ax.scatter(x=temp.index, y=temp.hashtag_score, s=75, color='firebrick', alpha=0.7)
	# Title, Label, Ticks and Ylim
	ax.set_title('Terrorist Hashtags Network Belonging Score of the Tweets', fontdict={'size':22})
	ax.set_ylabel('Number of Terrorist Hashtags' )
	ax.set_ylabel('Tweets')
	ax.set_xticks(temp.index)
	ax.set_xticklabels(temp.names.str.upper(), rotation=90, fontdict={'horizontalalignment': 'right', 'size':12})
	ax.set_ylim(0, 10)
	# Annotate
	for row in temp.itertuples():
		ax.text(row.Index+0.01, row.hashtag_score+0.15,rotation=90, s=round(row.hashtag_score, 2), horizontalalignment= 'center', verticalalignment='bottom', fontsize=14)
	plt.show()

def pie_chart_hashtags_terrorist(data):
	plt.rcParams['figure.figsize'] = [9, 6]
	temp = data[data['hashtag_score']>0].reset_index(drop=True)  
	p=0
	n=0
	o=0
	for i in range(len(temp)):
		if temp['polarity'].iloc[i]>0.1:
			p+=1
		elif temp['polarity'].iloc[i]<-0.1:
			n+=1
		else:
			o+=1
	f=0
	op=0
	for i in range(len(temp)):
		if temp['subjectivity'].iloc[i]>0.5:
			op+=1
		else:
			f+=1

	labels = 'Positive', 'Negative','Neutral'
	sizes = [p,n,o]
	colors = ['yellowgreen','red', 'gold'] #, 'yellowgreen', 'lightcoral','lightskyblue',
	explode = (0, 0,0)  # explode 1st slice
	labels2='Opinion','Fact'
	sizes2=[f,op]
	colors2=['lightblue','yellow']
	explode2=(0,0)
	fig, (ax1, ax2) = plt.subplots(1, 2)
	# Plot
	ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
	ax2.pie(sizes2, explode=explode2, labels=labels2, colors=colors2, autopct='%1.1f%%', shadow=True, startangle=140)
	plt.title('From '+str(len(data))+' tweets, '+ str(len(temp))+' tweets are following Terroristic Hashtags')
	plt.axis('equal')
	plt.show() 

def terrorist_tweets_classification_pieChart(data):

    plt.rcParams['figure.figsize'] = [9, 6]

    po = data["positive_opinion"]
    pf = data["positive_fact"]
    neu = data["neutral"]
    nf = data["negative_fact"]
    no = data["negative_opinion"]
    labels = 'Positive opinion', 'Positive fact','Neutral','Negative fact','Negative opinion'
    sizes = [po,pf,neu,nf,no]
    colors = ['blue','red', 'gold','yellowgreen', 'lightcoral']
    explode = (0,0,0,0,0)  # explode 1st slice

    fig, (ax1) = plt.subplots(1, 1)
    # Plot
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title('Sentiment of the tweets with terrostic contents')
    plt.axis('equal')
    plt.show()	
	
def distribution_sentiment_terrorist_tweets(tweets_df):
    ### VISUALIZATION
    plt.rcParams['figure.figsize'] = [20, 12]
    for i in range (len(tweets_df)):
      if tweets_df["terrorist_suggestion"].iloc[i] != 0:
        x=tweets_df.polarity.iloc[i]
        y=tweets_df.subjectivity.iloc[i]
        if x>0.1 : # blue   red
          if y>0.5:  # yellow   green
            plt.scatter(x,y, color='blue')
          else: 
            plt.scatter(x,y, color='pink')
        elif -0.1<=x<=0.1:
          plt.scatter(x,y, color='gold')
        else:
          if y>0.5:  # yellow   green
            plt.scatter(x,y, color='purple')
          else: 
            plt.scatter(x,y, color='red')  
    plt.xlim(-1,1)
    plt.ylim(0,1)
    plt.title('Scatter plot of sentiment analysis for terrorist contents',fontsize=20)
    plt.xlabel('<------------------ NEGATIVE ------------------   POLARITY ------------------ POSITIVE ------------------>',fontsize=15)
    plt.ylabel('<----------------- FACTS ------------------ SUBJECTIVITY ------------------ OPINIONS ----------------->',fontsize=15)
    plt.show()

  
  