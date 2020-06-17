#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 15:07:55 2020

@author: mike
"""
# import os
# import selenium
# import datetime
import pandas as pd
import numpy as np
from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
from time import sleep
from io import StringIO
from pycliflo.datasets_mapping import Datasets
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

pd.options.display.max_columns = 10

#############################
### Parameters

datasets_dict = {'181': 'rain_fixed_periods', '182': 'rain_fixed_periods', '185': 'rain_fixed_periods', '261': 'snow', '131': 'surface_wind', '132': 'surface_wind', '133': 'surface_wind', '134': 'surface_wind', '201': 'max_min_temp', '202': 'max_min_temp', '203': 'max_min_temp', '204': 'max_min_temp', '205': 'max_min_temp', '206': 'max_min_temp', '151': 'sunshine', '152': 'sunshine', '161': 'radiation', '162': 'radiation', '163': 'radiation', '164': 'radiation', '166': 'radiation', '167': 'radiation', '121': 'pressure', '122': 'pressure', '123': 'pressure', '124': 'pressure', '125': 'pressure', '126': 'pressure', '127': 'pressure', '171': 'evaporation', '172': 'evaporation', '173': 'evaporation', '174': 'evaporation', '175': 'evaporation', '231': 'soil_moisture'}

code_ops = list(datasets_dict.keys())

inv_map = {}
for k, v in datasets_dict.items():
    inv_map[v] = inv_map.get(v, [])
    inv_map[v].append(k)

site_details_url = 'https://cliflo.niwa.co.nz/pls/niwp/wstn.stn_details?cagent={}'

############################################
### Main class


class Cliflo(object):

    def __init__(self, chrome_driver_path):
        """

        """
        self._Datasets = Datasets

        self.chromedriver = chrome_driver_path

        pass

    @staticmethod
    def _date_range(driver, from_date, to_date):
        """

        """
        fdate = pd.Timestamp(from_date)
        tdate = pd.Timestamp(to_date)

        fyear = fdate.year
        fmonth = fdate.month
        fday = fdate.day
        fhour = fdate.hour

        tyear = tdate.year
        tmonth = tdate.month
        tday = tdate.day
        thour = tdate.hour

        names = {'date1_1': fyear, 'date1_2': fmonth, 'date1_3': fday, 'date1_4': fhour, 'date2_1': tyear, 'date2_2': tmonth, 'date2_3': tday, 'date2_4': thour}

        for d, val in names.items():
            if val > 0:
                date_box = driver.find_element_by_name(d)
                date_box.clear()
                date_box.send_keys(str(val))


    ########################################3
    ### measurement type codes


    def get_dataset_codes(self, available=True):
        """

        """

        datasets_url = 'https://cliflo.niwa.co.nz/pls/niwp/wa.list_codes'

        r1 = requests.get(datasets_url)

        soup = BeautifulSoup(r1.text, 'html.parser')

        list1 = []
        for s in soup.findAll('tr')[1:]:
            list2 = []
            for d in s.findAll():
                list2.extend([d.text])
            list1.append(list2)

        cols = ['Code', 'Code Description', 'Code Full Description']

        niwa_codes_all = pd.DataFrame(list1, columns=cols)
        niwa_codes = niwa_codes_all[niwa_codes_all.Code.isin(code_ops)].reset_index(drop=True).copy()

        self.dataset_codes = niwa_codes

        if available:
            return niwa_codes
        else:
            return niwa_codes_all


    def _assign_datasets(self, driver, dataset_code):
        """

        """
        ## Run checks
        if not isinstance(dataset_code, str):
            raise ValueError('dataset_code must be a str')
        else:
            dataset_code = [dataset_code]

        code_ops = list(datasets_dict.keys())
        check_codes = [i in code_ops for i in dataset_code]

        if not all(check_codes):
            raise ValueError('Wrong code(s) entered. Run the get_dataset_types method ')

        ## Filter and Assign
        ds1 = set([datasets_dict[d] for d in dataset_code])
        ds2 = {k: v for k, v in inv_map.items() if k in ds1}
        ds3 = {}
        for k, v in ds2.items():
            v1 = [i for i in v if i in dataset_code]
            ds3.update({k: v1})

        code_fun = self._Datasets()

        for name in ds3:
            fun1 = getattr(code_fun, name)
            fun1(driver, ds3[name])


    def get_sites(self, dataset_code, lat=-43.874770, lon=170.952955, distance=200, timeout=30, sites_op='or', site_owner=False):
        """

        """

        ### Open headless Chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome(self.chromedriver, options=options)

        ### Open main Cliflo site as a public login
        driver.get('https://cliflo.niwa.co.nz/pls/niwp/wgenf.genform1')

        ### Dataset codes
        self._assign_datasets(driver, dataset_code)

        ### Get the sites
        choose_st = driver.find_element_by_name('agent')
        choose_st.click()

        driver.switch_to.window(driver.window_handles[1])

        if sites_op == 'and':
            and_radio = driver.find_element_by_xpath("//input[@value='and']")
            and_radio.click()

        lat_lon_radio = driver.find_element_by_xpath("//input[@value='latlongc']")
        lat_lon_radio.click()

        lat_box = driver.find_element_by_name('clat1')
        lat_box.clear()
        lat_box.send_keys(str(lat))

        lon_box = driver.find_element_by_name('clong1')
        lon_box.clear()
        lon_box.send_keys(str(lon))

        rad_box = driver.find_element_by_name('crad')
        rad_box.clear()
        rad_box.send_keys(str(distance))

        download_field = driver.find_element_by_xpath("//option[@value='texttab']")
        download_field.click()

        submit_box = driver.find_element_by_name('Submit')
        submit_box.click()

        driver.switch_to.window(driver.window_handles[2])
        print('Please wait for the sites page to load...')
        sleep(2)

        timer = int(timeout/3)
        while timer > 0:
            try:
                sites1 = pd.read_table(StringIO(driver.page_source), skiprows=6, skipfooter=2, engine='python')
                break
            except:
                timer = timer - 1
                if timer == 0:
                    driver.quit()
                    raise ValueError('Sites page took too long to load. Please reduce the distance and try again.')
                sleep(3)

        driver.quit()

        sites1['Start_Date'] = pd.to_datetime(sites1['Start_Date'], dayfirst=True, infer_datetime_format=True)
        sites1['End_Date'] = pd.to_datetime(sites1['End_Date'], dayfirst=True, infer_datetime_format=True)

        if site_owner:
            print('Getting site owner...this may take a minute...')
            agents1 = sites1.Agent.unique()
            lst1 = []
            for a in agents1:
                owner1 = self.get_site_owner(a)
                lst1.append([a, owner1])
            owner2 = pd.DataFrame(lst1, columns=['Agent', 'Owner'])
            owner2.loc[owner2.Owner == 'N/A', 'Owner'] = np.nan
            sites1 = pd.merge(sites1, owner2, on='Agent')

        self.sites_dis = sites1

        return sites1


    def login(self, username, password):
        """

        """
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome(self.chromedriver, options=options)

        ### Open main Cliflo site for login
        driver.get('https://cliflo.niwa.co.nz')

        ### Log in
        user_box = driver.find_element_by_name('cusername')
        user_box.clear()
        user_box.send_keys(username)

        pass_box = driver.find_element_by_name('cpwd')
        pass_box.clear()
        pass_box.send_keys(password)

        submit_box = driver.find_element_by_name('submit')
        submit_box.click()

        sleep(6)

        self.driver = driver
        print('logged in')


    def logout(self):
        """

        """
        self.driver.quit()
        delattr(self, 'driver')
        print('logged out')


    def get_ts_data(self, dataset_code, site, from_date, to_date, timeout=30):
        """

        """
        ### Open headless Chrome driver
        if hasattr(self, 'driver'):
            driver = self.driver
        else:
            raise ValueError('You must be logged in to get ts data')

        ### Dataset codes
        if hasattr(self, 'dataset_code'):
            if self.dataset_code != dataset_code:
                self._assign_datasets(driver, dataset_code)
        else:
            self._assign_datasets(driver, dataset_code)
            self.dataset_code = dataset_code

        ### Assign sites
        if isinstance(site, str):
            site = [site]
        if not isinstance(site, list):
            raise ValueError('site must be either a str or list of str')

        site_str = ','.join(site)
        agents_box = driver.find_element_by_name('agents')
        agents_box.clear()
        agents_box.send_keys(site_str)

        ### Assign dates
        self._date_range(driver, from_date, to_date)

        ### Assign File format
        format_box = driver.find_element_by_xpath("//option[@value='texttab']")
        format_box.click()

        ### Submit!
        submit_box = driver.find_element_by_name('submit_sq')
        submit_box.click()

        print('Please wait for the sites page to load...')
        sleep(2)

        ### Get the data
        timer = int(timeout/3)
        while timer > 0:
            try:
                page = driver.page_source
                if len(page) > 20:
                    break
            except:
                timer = timer - 1
                if timer == 0:
                    driver.quit()
                    raise ValueError('Page took too long to load. Please reduce the request size.')
                sleep(3)

        driver.back()
        sleep(1)

        self.page_source = page

        ## Sites
        s_index1 = page.find('Name')
        s_index2 = page.find('Note: ')
        sites_str = StringIO(page[s_index1:(s_index2 - 1)])

        sites1 = pd.read_table(sites_str)

        self.sites = sites1

        ## TS data
        rc_index = page.find('Total number of rows output')

        page_ts = page[s_index2:(rc_index - 1)]

        if page_ts == '':
            raise ValueError('No useful time series returned')

        site_index1 = page_ts.find('Station')
        site_index2 = page_ts.find('Station', site_index1+1)
        if site_index2 == -1:
            ts_str = page_ts[site_index1:]
            footer = 1
        else:
            ts_str = page_ts[site_index1:(site_index2 - 1)]
            footer = 2

        ts_str1 = StringIO(ts_str)
        ts1 = pd.read_table(ts_str1, skipfooter=footer, engine='python')
        if ts1.empty:
            raise IndexError('No time series data was returned. This likely means that the time range is incorrect or that the data is not public. See the following for details:  https://cliflo.niwa.co.nz/pls/niwp/wh.do_help?id=nodata')
        ts1['DatasetCode'] = dataset_code
        ts2 = ts1.set_index(['Station', 'DatasetCode', 'Date(NZST)']).stack().reset_index()
        ts2.rename(columns={'level_3': 'Parameter', 0: 'Value'}, inplace=True)

        ts_df = ts2.copy()

        ts_df['Date(NZST)'] = pd.to_datetime(ts_df['Date(NZST)'], format='%Y%m%d:%H%M')
        ts_df.loc[ts_df.Value == '-', 'Value'] = np.nan

        self.ts_data = ts_df

        ## Number of rows left
        rr_index = page.find('Number of rows remaining in subscription')
        copy_index = page.find('Copyright NIWA')
        rr = int(page[(rr_index + 43):(copy_index - 1)])
        print('You have ' + str(rr) + ' remaining rows')
        self.remaining_rows = rr

        ## Return
        return sites1, ts_df


    @staticmethod
    def get_site_owner(site):
        """

        """
        r1 = requests.get(site_details_url.format(str(site)))
        c1 = str(r1.content)
        auth_index = c1.find('Observing Authority')
        c2 = c1[auth_index:]
        i2 = c2.find('extrdata')
        c3 = c2[(i2 + 10):]
        name = c3[:c3.find('<')]

        return name
