#!/usr/bin/env python

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException        
from win10toast import ToastNotifier
import platform
import os
import argparse
import getpass
import time


def putAttendance(driverUrl,webinarLink,email,name,regno,phno,batch,dept):
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
            toaster = ToastNotifier()
            toaster.show_toast("Attendance Posted",attendanceLink.text)
            # attendanceLink.click()
            browser.get(attendanceLink.text)
            email_element = browser.find_element_by_xpath("//input[@aria-label='Your email']")
            email_element.send_keys(email)
            college_element = browser.find_element_by_xpath("//div[@data-value='SSN College Of Engineering']")
            college_element.click()
            name_element = browser.find_element_by_xpath("//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")
            name_element.send_keys(name)
            register_number_element = browser.find_element_by_xpath("//*[@id='mG61Hd']/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input")
            register_number_element.send_keys(regno)
            mobile_number_element = browser.find_element_by_xpath("//*[@id='mG61Hd']/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input")
            mobile_number_element.send_keys(phno)
            batch_element = browser.find_element_by_xpath("//*[@id='mG61Hd']/div[2]/div/div[2]/div[6]/div/div/div[2]/div[1]/div/span/div/div[{}]".format(batch))
            batch_element.click()
            department_element = browser.find_element_by_xpath("//*[@id='mG61Hd']/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div/span/div/div[{}]".format(dept))
            department_element.click()
            content_element = browser.find_element_by_xpath("//*[@id='mG61Hd']/div[2]/div/div[2]/div[8]/div/div/div[2]")
            content_element.click()
            training_day_count = browser.find_element_by_xpath("//*[@id='mG61Hd']/div[2]/div/div[2]/div[9]/div/div/div[2]")
            training_day_count.click()
            day_element = browser.find_element_by_xpath("//*[@id='mG61Hd']/div[2]/div/div[2]/div[10]/div/div/div[2]/div/div")
            day_element.click()
            lecture_1_element = browser.find_element_by_xpath("//*[@id='mG61Hd']/div[2]/div/div[2]/div[11]/div/div/div[2]/div/div/span/div/div[1]")
            lecture_1_element.click()
            lecture_2_element = browser.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[12]/div/div/div[2]/div/div/span/div/div[1]/label')
            lecture_2_element.click()
            submit_button = browser.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[3]/div[1]/div')
            submit_button.click()
            print("FORM SUBMITTED")
            time.sleep(10)
            browser.close()
            exit()
        except NoSuchElementException:
            continue

def main():
    parser = argparse.ArgumentParser(prog='Webinar Jam Attendance Bot',
    usage='''
     please specify the following :
     --driver  =  location of the selenium driver
     --webinar =  url of the webinar that you want to post attendance
     --email   =  specify your email to be filled in  form
     --name    = name to be filled in form
     --regno   = regno to be filled in form
     --phno    = phone number to be filled in the form
     --batch   = specify the number 1 to 4 only
     --dept    = specify the department which you belong to \n\t\t 1 for CSE \n\t\t 2 for IT \n\t\t 3 for ECE \n\t\t 4 for EEE \n\t\t 5 for Mechanical \n\t\t 6 for Civil \n\t\t 7 for Chemical \n\t\t 8 for Chemical
    ''',
    description='''
    -------------------------------------------------------------------------------------------------------------------------
    Description :
        This tool is for the automation of the attendance in webinarJam mainly for ssn student's sixphrase classes
    ''',
    epilog="Copyrights @ JayVishaalJ",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    add_help=True
    )
    parser.add_argument("--driver","-d",type=str,help="Enter the location of the web driver",metavar="DRIVER LOCATION",required=True)
    parser.add_argument("--webinar","-w",type=str,help="Enter the url of the webinar",metavar="WEBINAR LINK",required=True)
    parser.add_argument("--email","-e",type=str,help="Enter your email to be filled in  form",metavar="EMAIL ID",required=True)
    parser.add_argument("--name","-n",type=str,help="Enter your name to be filled in  form",metavar="NAME",required=True)
    parser.add_argument("--regno","-r",type=str,help="Enter your register number to be filled in  form",metavar="REGISTER ID",required=True)
    parser.add_argument("--phno","-p",type=str,help="Enter your phone number to be filled in  form",metavar="PHONE NUMBER",required=True)
    parser.add_argument("--batch","-b",type=str,help="Enter your batch number 1 to 4 only",metavar="EMAIL ID",required=True)
    parser.add_argument("--dept","-dp",type=str,help="Enter the the department which you belong to \n\t\t 1 for CSE \n\t\t 2 for IT \n\t\t 3 for ECE \n\t\t 4 for EEE \n\t\t 5 for Mechanical \n\t\t 6 for Civil \n\t\t 7 for Chemical \n\t\t 8 for Chemical",metavar="EMAIL ID",required=True)
    
    arg = parser.parse_args()
    putAttendance(arg.driver,arg.webinar,arg.email,arg.name,arg.regno,arg.phno,arg.batch,arg.dept)
    

if __name__ == '__main__':
    main()