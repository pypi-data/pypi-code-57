from .general import GeneralData

import time
import datetime
import os

from pathlib import Path

import csv


class PlainText(GeneralData):

    def __init__(self, **kwargs):
        super(PlainText, self).__init__()
        code=kwargs['code']
        ext=kwargs['info']
        self.code=code
        self.folder=kwargs['path']
        self.path_file=''
        self.source = self.filename(code)
        self.ext = ext
        self.header = []
        self.path = Path(self.path_file)
        if not self.path.exists():
            os.makedirs(str(self.path))
        self.sep = ';'
        self.time_format = "%Y%m%d_%H%M%S"
        self.time_col = ''

    def filename(self, code):
        time_format = "%Y%m%d_%H%M%S"
        self.timestamp = datetime.datetime.fromtimestamp(
            time.time()).strftime(time_format)
        self.name = self.timestamp
        # check path  if exists and ts folder 
        self.path_file = self.folder + "/" + self.name
        return self.path_file

    def set_source(self, value):
        self.filename(value)

    def save_data(self, data):
        self.header=data[1].keys()
        separator = self.sep
        message = data[1]
        list_values = []
        # Data is a dict with a list of tables
        for k in self.header:
            list_values.append(message[k])
        #print(self.code)
        #print(list_values)
        #line = separator.join(map(str, list_values))
        wline = message
        filename=self.source+"/"+data[0]+"."+self.ext
        fexists=os.path.isfile(filename)
        if not fexists:
            var='w'
        else:
            var='a'
        with open(filename, var) as csvfile:
            writer = csv.DictWriter(csvfile,
                                    fieldnames=self.header, delimiter=self.sep)
            #print(wline)
            if not fexists:
                writer.writeheader()
                fexists=os.path.isfile(filename)
            if fexists:
                writer.writerow(wline)

    def check_data(self):
        # get id_col by col_name, name of time col
        self.data = []
        with open(self.path_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=self.header)
            for row in reader:
                yield row
                self.data.append(row)
        return self.data

    def show_data(self, time, table, columns):
        t0 = time[0]
        t1 = time[1]
        k = 0
        select = []
        while True:
            if t0 >= self.data[k][self.time_col]:
                self.ind_0 = k
            if t1 > self.data[k][self.time_col]:
                self.ind_0 = k
                break
            k += 1
        test = all(x in self.header for x in columns)
        for q in range(self.ind_0, self.ind_1):
            if test:
                result = [self.data[q][x] for x in columns]
                select.append(result)
                #print(result)
        return select

    def show_info(self):
        print("Source")
        print(self.source)
        print("Header")
        print(self.header)
        print("Path")
        print(self.path)
        print("Field Separator")
        print(self.sep)
        print("Time Format")
        print(self.time_format)
