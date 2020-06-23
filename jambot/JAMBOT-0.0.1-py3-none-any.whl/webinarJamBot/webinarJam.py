#!/usr/bin/env python

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException        
# from win10toast import ToastNotifier
import platform
import os
import argparse
import getpass


def putAttendance(driverUrl,webinarLink):
    options = webdriver.ChromeOptions()
    print(platform.system())
    if(platform.system() == "Windows"):
        localAppDataURI = 'C:/Users/'+getpass.getuser()+'/AppData/Local/Google/Chrome/User Data/Default'
        localAppDataURI = localAppDataURI.replace('\\','/')
        print(localAppDataURI)
    elif(platform.system() == "Linux"):
        localAppDataURI = '/home/'+getpass.getuser()+'/.config/google-chrome/default'
        localAppDataURI = localAppDataURI.replace('\\','/')
        print(localAppDataURI)
    #/Users/<username>/Library/Application Support/Google/Chrome/Default

    options.add_argument('--user-data-dir={}'.format(localAppDataURI))
    options.add_argument('--profile-directory=Default')
    browser = webdriver.Chrome(executable_path=driverUrl,options=options)
    browser.get(webinarLink)
    while True:
        try:
            attendanceLink = browser.find_element_by_css_selector('a.inline-link')
            print("ATTENDANCE POSTED : "+attendanceLink.text)
            # toaster = ToastNotifier()
            # toaster.show_toast("Attendance Posted",attendanceLink.attendanceLink.text)
            attendanceLink.click()
            break
        except NoSuchElementException:
            continue

def main():
    parser = argparse.ArgumentParser(prog='Webinar Jam Attendance Bot',
    usage='''
     please specify the following :
     --driver  =  location of the selenium driver
     --webinar =  url of the webinar that you want to post attendance
    ''',
    description='''
    ------------------------------------------------------------------------------------
    Description :
        This tool is for the automation of the attendance in webinarJam mainly for ssn student's sixphrase classes
    ''',
    epilog="Copyrights @ JayVishaalJ",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    add_help=True
    )
    parser.add_argument("--driver","-d",type=str,help="Enter the location of the web driver",metavar="DRIVER LOCATION",required=True)
    parser.add_argument("--webinar","-w",type=str,help="Enter the url of the webinar",metavar="WEBINAR LINK",required=True)
    arg = parser.parse_args()
    putAttendance(arg.driver,arg.webinar)
    

if __name__ == '__main__':
    main()
# string = "C:\\Users\\jayvi\\pythonAutomation\\webAutomation\\dependencies\\chromedriver.exe"
# putAttendance(string)