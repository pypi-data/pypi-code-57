#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 07:44:39 2020

@author: mike
"""
from time import sleep


######################################
### dataset code mappings


class Datasets:

    @staticmethod
    def rain_fixed_periods(driver, code):
        """

        """
        code_ops = ['181', '182', '185']
        if isinstance(code, str):
            code = [code]

        check = [i in code_ops for i in code]

        if not all(check):
            raise ValueError('Wrong code used')

        driver.get('https://cliflo.niwa.co.nz/pls/niwp/wgenf.genform1?cdt=ls_ra&cadd=t')

        freq_box = driver.find_element_by_xpath("//input[@value='181']")
        freq_box.click()

        for i in code:
            freq_box = driver.find_element_by_xpath("//input[@value='{}']".format(i))
            freq_box.click()

        sleep(1)

    @staticmethod
    def snow(driver, code='261'):
        """

        """
        driver.get('https://cliflo.niwa.co.nz/pls/niwp/wgenf.genform1?cdt=ls_ra&cadd=t')

        sleep(1)

    @staticmethod
    def surface_wind(driver, code):
        """

        """
        code_ops = ['131', '132', '133', '134']
        if isinstance(code, str):
            code = [code]

        check = [i in code_ops for i in code]

        if not all(check):
            raise ValueError('Wrong code used')

        driver.get('https://cliflo.niwa.co.nz/pls/niwp/wgenf.genform1?cdt=ls_sfw&cadd=t')

        freq_box = driver.find_element_by_xpath("//input[@value='132']")
        freq_box.click()

        for i in code:
            freq_box = driver.find_element_by_xpath("//input[@value='{}']".format(i))
            freq_box.click()

        sleep(1)

    @staticmethod
    def max_min_temp(driver, code):
        """

        """
        code_ops = ['201', '202', '203', '204', '205', '206']
        checked = '201'
        if isinstance(code, str):
            code = [code]

        check = [i in code_ops for i in code]

        if not all(check):
            raise ValueError('Wrong code used')

        driver.get('https://cliflo.niwa.co.nz/pls/niwp/wgenf.genform1?cdt=ls_mxmn&cadd=t')

        freq_box = driver.find_element_by_xpath("//input[@value='{}']".format(checked))
        freq_box.click()

        for i in code:
            freq_box = driver.find_element_by_xpath("//input[@value='{}']".format(i))
            freq_box.click()

        sleep(1)

    @staticmethod
    def sunshine(driver, code):
        """

        """
        code_ops = ['151', '152']
        checked = '151'
        if isinstance(code, str):
            code = [code]

        check = [i in code_ops for i in code]

        if not all(check):
            raise ValueError('Wrong code used')

        driver.get('https://cliflo.niwa.co.nz/pls/niwp/wgenf.genform1?cdt=ls_sun&cadd=t')

        freq_box = driver.find_element_by_xpath("//input[@value='{}']".format(checked))
        freq_box.click()

        for i in code:
            freq_box = driver.find_element_by_xpath("//input[@value='{}']".format(i))
            freq_box.click()

        sleep(1)

    @staticmethod
    def radiation(driver, code):
        """

        """
        code_ops = ['161', '162', '163', '164', '166', '167']
        checked = '161'
        if isinstance(code, str):
            code = [code]

        check = [i in code_ops for i in code]

        if not all(check):
            raise ValueError('Wrong code used')

        driver.get('https://cliflo.niwa.co.nz/pls/niwp/wgenf.genform1?cdt=ls_rad&cadd=t')

        freq_box = driver.find_element_by_xpath("//input[@value='{}']".format(checked))
        freq_box.click()

        for i in code:
            freq_box = driver.find_element_by_xpath("//input[@value='{}']".format(i))
            freq_box.click()

        sleep(1)

    @staticmethod
    def pressure(driver, code):
        """

        """
        code_ops = ['121', '122', '123', '124', '125', '126', '127']
        checked = '121'
        if isinstance(code, str):
            code = [code]

        check = [i in code_ops for i in code]

        if not all(check):
            raise ValueError('Wrong code used')

        driver.get('https://cliflo.niwa.co.nz/pls/niwp/wgenf.genform1?cdt=ls_press&cadd=t')

        freq_box = driver.find_element_by_xpath("//input[@value='{}']".format(checked))
        freq_box.click()

        for i in code:
            freq_box = driver.find_element_by_xpath("//input[@value='{}']".format(i))
            freq_box.click()

        sleep(1)

    @staticmethod
    def evaporation(driver, code):
        """

        """
        code_ops = ['171', '172', '173', '174', '175']
        checked = '171'
        if isinstance(code, str):
            code = [code]

        check = [i in code_ops for i in code]

        if not all(check):
            raise ValueError('Wrong code used')

        driver.get('https://cliflo.niwa.co.nz/pls/niwp/wgenf.genform1?cdt=ls_evap&cadd=t')

        freq_box = driver.find_element_by_xpath("//input[@value='{}']".format(checked))
        freq_box.click()

        for i in code:
            freq_box = driver.find_element_by_xpath("//input[@value='{}']".format(i))
            freq_box.click()

        sleep(1)

    @staticmethod
    def soil_moisture(driver, code='231'):
        """

        """
        driver.get('https://cliflo.niwa.co.nz/pls/niwp/wgenf.genform1?cdt=ls_soilm&cadd=t')

        sleep(1)