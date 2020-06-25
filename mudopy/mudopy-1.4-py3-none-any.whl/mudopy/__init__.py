from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
from bs4 import BeautifulSoup
import requests
from pathlib import Path
import urllib.request
new_url=None
noterror=True
class InvalidPathException(Exception):
    pass
def set_path(path):
    """Add path of selenium driver"""
    try:
        driver = webdriver.Chrome(path)
        driver.quit()
        file = open("drpth.txt","w")
        file.write(path)
        file.close()
    except:
        raise InvalidPathException("Cannot find driver at %s"%path)
def fetch_url(url):
    sc = requests.get(url)
    sctext = sc.text
    
    time.sleep(2)
    soup = BeautifulSoup(sctext,"html.parser")
    songs = soup.findAll("div",{"class":"yt-lockup-video"})
    return songs

def download(song, artist = None, down_path = None, play_after_downloading = True):
    
    global new_url,noterror
    if artist:
        song = song+" by "+artist  
    print(song)
    url = 'https://www.youtube.com/results?q=' + song

    music=fetch_url(url)
    n=len(music)
    #print(n)
    count=0
    while n<1:
        music=fetch_url(url)
        n=len(music)
        count+=1
        
        if count>10:
            print("Sorry! song not found")
            noterror=False
            break
        print("Searching song Try %d"%count)
    
    #print(url,down_pth)
    if noterror:
        song_content = music[0].contents[0].contents[0].contents[0] 
        songurl = song_content["href"]

        url = "https://www.youtube.com"+songurl
        print("Downloading")
        if not down_path:
            down_path = os.getcwd()
        file = open("drpth.txt")
        dripth = file.read()
        
        chromeOptions=Options()
        chromeOptions.add_experimental_option("prefs",{"download.default_directory":down_path})
        chromeOptions.add_argument("--headless")
        driver=webdriver.Chrome(dripth,options=chromeOptions)
        driver.get("https://ytmp3.cc/en13/")
        #driver.maximize_window()
        driver.find_element_by_xpath("//*[@id='mp3']").click()
        driver.find_element_by_xpath("//*[@id='input']").send_keys(url)
        driver.find_element_by_xpath("//*[@id='submit']").click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="buttons"]/a[1]').click()
        old_lst = os.listdir(down_path)
        while True:
            new_lst = os.listdir(down_path)
                
            if new_lst != old_lst:
                song = set(new_lst) - set(old_lst)
                song = str(song)
                song = song.replace("{","")
                song = song.replace("}","")
                song = song.strip("'")
                
                if Path(song).suffix == '.mp3':
                    driver.quit()
                    if play_after_downloading:
                        print("Downloaded to %s"%down_path)
                        print("playing")
                        os.startfile(down_path+"/"+song)
                    return "Song downloaded"
                    break

try:
    file = open("drpth.txt")

except:
    file = open("drpth.txt","w")
    print("Hello from the creator of Mudopy, Smit Parmar and Ankit Raj Mahapatra, do report bug if any")
    file.close()
