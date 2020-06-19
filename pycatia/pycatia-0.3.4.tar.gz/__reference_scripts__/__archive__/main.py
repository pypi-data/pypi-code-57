from bs4 import BeautifulSoup
import pyautogui
import pyperclip
import requests
from selenium import webdriver
import tkinter as tk
from pathlib import Path
import os
import time

import inflection

base_url = "http://evereux.uk/catia_doc/r28/interfaces/"
root_url = "http://evereux.uk/catia_doc/r28/interfaces/_index/main.htm"
base_folder = Path(os.getcwd(), 'v5automation_files_r28_extracted')

root = tk.Tk()
root.withdraw()


driver = webdriver.Firefox()
# driver.get("http://evereux.uk/catia_doc/r28/interfaces/CATGSMIDLItf/interface_HybridShapeSweepCircle_32736.htm")
#
# body = driver.find_element_by_tag_name("Body")
# text = body.get_attribute('innerHTML')

# pyautogui.click(1276, 322)
# pyautogui.hotkey('ctrl', 'a')
# pyautogui.hotkey('ctrl', 'c')
# text = root.clipboard_get()
#
#
# print(text)

root_page = requests.get(root_url)
soup = BeautifulSoup(root_page.text, 'html.parser')
soup = soup.ul
urls = soup.find_all('a')


def scrape_frame_work(url, folder_name):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    soup = soup.ul
    urls = soup.find_all('a')
    for url in urls:
        object_url = url['href']
        class_name = url.text.strip()
        object_url = base_url + object_url
        driver.get(object_url)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.1)
        text = root.clipboard_get()
        if class_name.lower() not in text.lower():
            raise ValueError(f'Problem with reading text to clipboard. {class_name} {text}')
        file_name = Path(folder_name, (inflection.underscore(class_name) + '.txt'))
        with open(file_name, 'w') as f:
            f.write(text)


if __name__ == '__main__':

    for url in urls:
        frame_work_url = base_url + url['href'].rsplit('/', 1)[1]
        print(f'Scanning {frame_work_url}.')
        
        folder_name = Path(base_folder, url.text.strip())
        if not folder_name.exists():
            folder_name.mkdir()
        scrape_frame_work(frame_work_url, folder_name)
