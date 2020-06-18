import re
import pandas as pd
import numpy as np
import os
import pytz
from datetime import datetime
import json

# logging
import logging
log = logging.getLogger()


def is_float(val):
    try:
        # if this isn't a numeric value, we'll cause a valueerror exception
        float(val)
        # don't allow NaN values, either.
        if pd.isnull(val):
            return False
        return True
    except:
        return False


''' classes '''


class PSenseParser:
    def __init__(self, filename='', exp_config=None, debugmode=False):
        self.debugmode = debugmode
        self.valid_types = ['BWII-DL', 'BWII-INST', 'BWII-MINI',
                            'PSHIELD', 'VFP', 'EXPLAIN',
                            'WEB1CHAN', 'WEB2CHAN', 'WEB3CHAN']
        self.header_text = {
            'BWII-DL': 'DATETIME,trace_record,rNUM,I1,VW1,VR1,VC1,SEN1_ON,DISC1,I2,VW2,VR2,VC2,SEN2_ON,DISC2,BATTV,BATTSTAT,TRACE_CODE,TRACE_EVENT',
            'BWII-INST': 'BWIIData',
            'BWII-MINI': 'DATETIME,trace_record,rNUM,I1,VW1,VC,SEN1_ON,DISC1,I2,VW2,SEN2_ON,DISC2,I3,VW3,SEN3_ON,DISC3,BATTV,BATTSTAT,TRACE_CODE,TRACE_EVENT',
            'PSHIELD': 'PotentiostatShield',
            'VFP': 'VFP600',
            'EXPLAIN': 'EXPLAIN',
            'WEB1CHAN': 'timestamp,Raw1,Vout1,Filt1',
            'WEB2CHAN': 'timestamp,Raw1,Vout1,Raw2,Vout2,Filt1,Filt2',
            'WEB3CHAN': 'timestamp,Raw1,Vout1,Raw2,Vout2,Raw3,Vout3,Filt1,Filt2,Filt3'
        }
        self.delimiter = {
            'BWII-DL': ',',
            'BWII-INST': ',',
            'BWII-MINI': ',',
            'PSHIELD': ',',
            'VFP': '\t',
            'EXPLAIN': '\t',
            'WEB1CHAN': ',',
            'WEB2CHAN': ',',
            'WEB3CHAN': ',',
        }
        self.loc_timestamp = {
            'BWII-DL': 0,
            'BWII-INST': 0,
            'BWII-MINI': 0,
            'PSHIELD': 1,
            'VFP': None,
            'EXPLAIN': 0,
            'WEB1CHAN': 0,
            'WEB2CHAN': 0,
            'WEB3CHAN': 0,
        }
        self.loc_vout = {
            'BWII-DL': [4, 5, 10, 11],
            'BWII-INST': [1, 3],
            'BWII-MINI': [4, 5, 9, 13],
            'PSHIELD': None,
            'VFP': [0],
            'EXPLAIN': [1],
            'WEB1CHAN': [2],
            'WEB2CHAN': [2, 4],
            'WEB3CHAN': [2, 4, 6],
        }
        self.loc_isig = {
            'BWII-DL': [3, 9],
            'BWII-INST': [2, 4],
            'BWII-MINI': [3, 8, 12],
            'PSHIELD': [2],
            'VFP': [1],
            'EXPLAIN': [2],
            'WEB1CHAN': [1],
            'WEB2CHAN': [1, 3],
            'WEB3CHAN': [1, 3, 5],
        }
        self.num_channels = {
            'BWII-DL': 2, #[7, 13],
            'BWII-INST': 2,
            'BWII-MINI': 3, #[6, 10, 14],
            'PSHIELD': 1,
            'VFP': 1,
            'EXPLAIN': 1,
            'WEB1CHAN': 1,
            'WEB2CHAN': 2,
            'WEB3CHAN': 3,
        }

        # what's the current offset between local and UTC?
        # assumes things are collected in PST/PDT
        self.local = pytz.timezone("America/Los_Angeles")
        self.time_offset = datetime.now(self.local).utcoffset()

        self.source = None
        self.data = None
        self.name = filename
        self.config = exp_config
        self.vout = None
        self.we_count = 1

    def force_source(self, source):
        "hard-code the input file-format (alt. to identify_file_source)"
        if source in self.valid_types:
            log.debug('forcing source to be type [{}]'.format(source))
            self.source = source
            self.we_count = self.num_channels[source]
        else:
            raise IOError('Invalid source ({}). Must be in list: {}'.format(
                source, self.valid_types))

    def identify_file_source(self, fpath=''):
        "read the file header to identify the file format"
        for cur in self.valid_types:
            if self.find_header_text(fpath, self.header_text[cur]):
                log.debug('file [{}] has source [{}]'.format(fpath, cur))
                self.source = cur
                self.we_count = self.num_channels[cur]
                return cur

        log.warning('file [{}] has no known source'.format(fpath))
        self.source = None
        return None

    def read_variable_header_file(self, fname, line, **kwargs):
        "helper function returns data in the form of tuple of (data, header)"
        header_text = ''
        with open(fname, 'r', encoding="utf8", errors='ignore') as f:
            pos = 0
            cur_line = f.readline()
            stripped = re.sub(r'\s', '', cur_line)
            while not stripped.startswith(line):
                if f.tell() == pos:
                    break
                pos = f.tell()
                cur_line = f.readline().strip()
                stripped = re.sub(r'\s', '', cur_line)
                header_text += cur_line

            f.seek(pos)
            if pos == os.path.getsize(fname):
                log.warning('unable to extract header: eof')
                return None, None

            log.debug('header extracted (len={})'.format(pos))
            return pd.read_csv(f, **kwargs), header_text

    def parse_record(self, row):
        "parse a single sensor data record assuming the detected file format"
        row = row.split(self.delimiter[self.source])
        if self.loc_timestamp[self.source] is not None:
            timestamp = row[self.loc_timestamp[self.source]]
        else:
            timestamp = (datetime.utcnow() + self.time_offset).isoformat('T')

        if self.loc_vout[self.source] is not None:
            vout = [float(row[x]) for x in self.loc_vout[self.source]]
        else:
            vout = [None] * len(self.loc_isig[self.source])

        enable = [True]
        isig = [float(row[x]) for x in self.loc_isig[self.source]]
        if self.we_count == 1:
            isig = isig[0]
            vout = vout[0]

        # custom modifications for specific source types
        if self.source == 'VFP':
            isig = isig * 1e9

        # KLUDGE:  BWII hardware v12011 uses an arbitrary timestamp. For real-time purposes, just use the current time.
        elif (self.source == 'BWII-DL'):
            timestamp = (datetime.utcnow() + self.time_offset).isoformat('T')
            # convert Vout = Vw - Vc, converted to volts.

            enable = [float(row[x+2])==1 for x in self.loc_vout[self.source]][1:]
            enable.pop(1)
            vout = [(vout[0] - vout[1]) / 1000, (vout[2] - vout[3]) / 1000]
        elif (self.source == 'BWII-MINI'):
            timestamp = (datetime.utcnow() + self.time_offset).isoformat('T')
            enable = [float(row[x+1])==1 for x in self.loc_vout[self.source]][1:]
            vout = [(vout[0] - vout[1]) / 1000, (vout[2] - vout[1]) / 1000, (vout[3] - vout[1]) / 1000]
        elif self.source == 'PSHIELD':
            timestamp = (datetime.utcfromtimestamp(float(timestamp)) + self.time_offset).isoformat('T')

        elif self.source == 'WEB1CHAN' or self.source == 'WEB2CHAN':
            timestamp = timestamp.replace(' ', 'T')

        if self.source == 'WEB2CHAN':
            enable = [True, True]

        if vout is None and self.vout is not None:
            vout = self.vout

        log.debug('[PSenseParser][parse_record] data: {}'.format([timestamp, vout, isig]))
        return [timestamp, vout, isig, enable]

    def update_props(self, data, period=None, vout=None):
        self.data = data

        if period is None:
            period = data['timestamp'].diff().median()
        self.period = period

        if vout is None:
            vout = data['vout1'].median()
        self.vout = vout

    def load_rawfile(self, fname, origin_timestamp, origin_is_end):
        """parse an entire sensor flat-file into pandas DataFrame.
        Different logic is implemented depending on the file format."""
        self.data = None

        log.debug('[PSenseParser][load_rawfile] {}'.format([fname, origin_timestamp, origin_is_end]))

        if self.source == 'PSHIELD':
            data, header = self.read_variable_header_file(
                fname,
                "SampleCount",
                sep=",",
                skiprows=[1],
                usecols=lambda x: x.upper().strip() in ['ELAPSED SECONDS', 'CURRENT(NA)'])

            # skip any corrupted rows (or pshield restarts)
            mask = data.applymap(is_float).all(1)
            data = data[mask]
            # rearrange and add columns
            data.columns = ['timestamp', 'signal1']

            # add in vout from the file
            v_out = float(
                re.search(r'Output Voltage:([\W\.0-9]+)', header).group()[15:])
            data['vout1'] = np.ones(len(data.index)) * v_out
            data['enable1'] = np.ones(len(data.index), dtype=bool)

            # adjust from UTC to PST
            data['timestamp'] = (pd.to_datetime(data['timestamp'], unit='s') + self.time_offset)
            self.update_props(
                data=data[['timestamp', 'vout1', 'signal1', 'enable1']],
                vout=v_out)
            return True
        elif (self.source == 'BWII-DL'):
            data, header = self.read_variable_header_file(
                    fname,
                    self.header_text[self.source],
                    sep=',',
                    skiprows=0,
                    usecols=lambda x: x.upper().strip() in [
                        'DATETIME', 'TRACE_RECORD', 'RNUM', 
                        'I1', 'VW1', 'VR1', 'SEN1_ON', 
                        'I2', 'VW2', 'VR2', 'SEN2_ON'])

            data.columns = ['timestamp', 'type', 'record', 
                'signal1', 'vw1', 'vr1', 'enable1', 
                'signal2', 'vw2', 'vr2', 'enable2']

            # get rid of extra whitespace (\t)
            data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            
            # get rid of non-sensor data (e.g. trace / event records)
            mask = data[['type']].applymap(lambda type: type == "sensor_record").all(1)
            data = data[mask]
            
            # float validation
            mask = data[['signal1', 'vw1', 'vr1', 'enable1', 'signal2', 'vw2', 'vr2', 'enable2']].applymap(is_float).all(1)
            data = data[mask]
            
            if origin_timestamp is not None:
                data['timestamp'] = data['record'].map(lambda x: int(x))
                try:
                    period = 1 / float(
                        re.search(r'sampling interval:  ([0-9-\.E]+)', header).group()[20:]) or 30
                except:
                    period = 30

                origin_timestamp = pd.Timestamp(origin_timestamp)
                if origin_is_end:  # make sure origin reflects the timestamp of the first record.
                    origin_timestamp -= pd.Timedelta(
                        seconds=(len(data.index) - 1) * period)

                data['timestamp'] = pd.to_datetime(
                    (np.asarray(data['timestamp']) - float(data['timestamp'].iloc[0])) * period,
                    unit='s',
                    origin=origin_timestamp
                )
            else:
                data['timestamp'] = pd.to_datetime(data['timestamp'])

            data['vout1'] = (data['vw1'] - data['vr1']) / 1000
            data['vout2'] = (data['vw2'] - data['vr2']) / 1000

            self.update_props(
                data=data[['timestamp', 'vout1', 'signal1', 'enable1', 'vout2', 'signal2', 'enable2']],
                vout=(data['vout1'].median(), data['vout2'].median()))

            return True
        elif (self.source == 'BWII-MINI'):
            data, header = self.read_variable_header_file(
                    fname,
                    self.header_text[self.source],
                    sep=',',
                    skiprows=0,
                    usecols=lambda x: x.upper().strip() in [
                        'DATETIME', 'TRACE_RECORD', 'RNUM', 
                        'I1', 'VW1', 'VC', 'SEN1_ON', 
                        'I2', 'VW2', 'SEN2_ON', 
                        'I3', 'VW3', 'SEN3_ON'])
            data.columns = ['timestamp', 'type', 'record', 
                'signal1', 'vw1', 'vc', 'enable1', 
                'signal2', 'vw2', 'enable2', 
                'signal3', 'vw3', 'enable3']
            
            # get rid of extra whitespace (\t)
            data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            
            # get rid of non-sensor data (e.g. trace / event records)
            mask = data[['type']].applymap(lambda type: type == "sensor_record").all(1)
            data = data[mask]

            # float validation
            mask = data[['signal1', 'vw1', 'vc', 'enable1', 'signal2', 'vw2', 'enable2', 'signal3', 'vw3', 'enable3']].applymap(is_float).all(1)
            data = data[mask]
            
            if origin_timestamp is not None:
                data['timestamp'] = data['record'].map(lambda x: int(x))
                try:
                    period = 1 / float(
                        re.search(r'sampling interval:  ([0-9-\.E]+)', header).group()[20:]) or 30
                except:
                    period = 30

                origin_timestamp = pd.Timestamp(origin_timestamp)
                if origin_is_end:  # make sure origin reflects the timestamp of the first record.
                    origin_timestamp -= pd.Timedelta(
                        seconds=(len(data.index) - 1) * period)

                data['timestamp'] = pd.to_datetime(
                    (np.asarray(data['timestamp']) - float(data['timestamp'].iloc[0])) * period,
                    unit='s',
                    origin=origin_timestamp
                )
            else:
                data['timestamp'] = pd.to_datetime(data['timestamp'])

            # compute vw - vc
            data['vout1'] = (data['vw1'] - data['vc']) / 1000
            data['vout2'] = (data['vw2'] - data['vc']) / 1000
            data['vout3'] = (data['vw3'] - data['vc']) / 1000
            self.update_props(
                data=data[['timestamp', 'vout1', 'signal1', 'enable1', 'vout2', 'signal2', 'enable2', 'vout3', 'signal3', 'enable3']],
                vout=(data['vout1'].median(), data['vout2'].median(), data['vout3'].median()))

            return True
        elif self.source == 'BWII-INST':
            data, header = self.read_variable_header_file(
                fname,
                'Timestamp,Vout1,Signal1,Vout2,Signal2',
                sep=',',
                usecols=lambda x: x.upper().strip() in ['TIMESTAMP', 'VOUT1', 'SIGNAL1', 'VOUT2', 'SIGNAL2'])

            data.columns = ['timestamp', 'vout1', 'signal1', 'vout2', 'signal2']
            
            # get rid of extra whitespace (\t)
            data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            
            # spoof the enable flag
            data['enable1'] = np.ones(len(data.index), dtype=bool)
            data['enable2'] = np.ones(len(data.index), dtype=bool)

            # convert units
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            data = data[['timestamp', 'vout1', 'signal1', 'enable1', 'vout2', 'signal2', 'enable2']]

            self.update_props(data=data, vout=(data['vout1'].median(), data['vout2'].median()))
            return True
        elif self.source == 'VFP':
            assert origin_timestamp is not None, '\terror: this file type requires a timestamp to be specified'

            data, header = self.read_variable_header_file(
                fname,
                "VoltageCurrent",
                sep="\t",
                skiprows=[1],
                usecols=lambda x: x.upper() in ['VOLTAGE', 'CURRENT'])

            period = 1 / float(
                re.search(r'FREQ\tQUANT\t([0-9-\.E]+)', header).group()[11:])

            origin_timestamp = pd.Timestamp(origin_timestamp).to_pydatetime()
            if origin_is_end:  # make sure origin reflects the timestamp of the first record.
                origin_timestamp -= pd.Timedelta(
                    seconds=(len(data.index) - 1) * period)

            mask = data.applymap(is_float).all(1)
            data = data[mask]

            data['timestamp'] = pd.to_datetime(
                np.asarray(data.index) * period,
                unit='s',
                origin=origin_timestamp
            )

            data.columns = ['vout1', 'signal1', 'timestamp']
            data = data[['timestamp', 'vout1', 'signal1']]
            # convert from scientific notation string to floats
            data['signal1'] = data['signal1'].astype(np.float64) * 1e9
            # spoof the enable flag
            data['enable1'] = np.ones(len(data.index), dtype=bool)

            self.update_props(data=data, vout=data['vout1'].median(), period=period)
            return True
        elif self.source == 'EXPLAIN':

            data, header = self.read_variable_header_file(
                fname,
                "PtTVf",
                sep="\t",
                skiprows=[1],
                usecols=lambda x: x.upper() in ['T', 'VF', 'IM'])

            # extract starting time
            date_start = re.search(
                r'DATE\tLABEL\t([\-\./0-9]+)', header).group()[11:]
            time_start = re.search(
                r'TIME\tLABEL\t([\.0-9:]+)', header).group()[11:]
            origin_timestamp = datetime.strptime(
                date_start + 'T' + time_start, '%m/%d/%YT%H:%M:%S')

            # remove corrupted data
            mask = data.applymap(is_float).all(1)
            data = data[mask]

            # rearrange and add columns
            data.columns = ['timestamp', 'vout1', 'signal1']

            # adjust from seconds elapsed to PST
            data['timestamp'] = pd.to_datetime(
                round(data['timestamp']),
                unit='s',
                origin=origin_timestamp)

            # convert from A to nA
            data['signal1'] = data['signal1'].astype(np.float64) * 1e9
            # spoof the enable flag
            data['enable1'] = np.ones(len(data.index), dtype=bool)

            # save
            self.update_props(data=data, vout=data['vout1'].median())
            return True
        elif self.source == 'WEB1CHAN':
            data, header = self.read_variable_header_file(
                fname,
                self.header_text['WEB1CHAN'],
                sep=",",
                usecols=lambda x: x.upper() in ['TIMESTAMP', 'RAW1', 'VOUT1'])

            # rearrange and add columns
            data.columns = ['timestamp', 'signal1', 'vout1']
            data = data[['timestamp', 'vout1', 'signal1']]
            # convert timestamp column to datetime
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            # spoof the enable flag
            data['enable1'] = np.ones(len(data.index), dtype=bool)

            self.update_props(data=data, vout=data['vout1'].median())
            return True
        elif self.source == 'WEB2CHAN':
            data, header = self.read_variable_header_file(
                fname,
                self.header_text['WEB2CHAN'],
                sep=",",
                usecols=lambda x: x.upper() in ['TIMESTAMP', 'RAW1', 'RAW2', 'VOUT1', 'VOUT2'])

            # rearrange and add columns
            data.columns = ['timestamp', 'signal1', 'vout1', 'signal2', 'vout2']
            # convert timestamps to datetime 
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            # spoof the enable flag
            data['enable1'] = np.ones(len(data.index), dtype=bool)
            data['enable2'] = np.ones(len(data.index), dtype=bool)

            data = data[['timestamp', 'vout1', 'signal1', 'enable1', 'vout2', 'signal2', 'enable2']]
            
            self.update_props(data=data, vout=(data['vout1'].median(), data['vout2'].median()))
            return True
        elif self.source == "WEB3CHAN":
            data, header = self.read_variable_header_file(
                fname,
                self.header_text['WEB3CHAN'],
                sep=",",
                usecols=lambda x: x.upper() in ['TIMESTAMP', 'RAW1', 'RAW2', 'RAW3', 'VOUT1', 'VOUT2', 'VOUT3'])

            # rearrange and add columns
            data.columns = ['timestamp', 'signal1', 'vout1', 'signal2', 'vout2', 'signal3', 'vout3']
            # convert timestamps to datetime 
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            # spoof the enable flag
            data['enable1'] = np.ones(len(data.index), dtype=bool)
            data['enable2'] = np.ones(len(data.index), dtype=bool)
            data['enable3'] = np.ones(len(data.index), dtype=bool)

            data = data[['timestamp', 'vout1', 'signal1', 'enable1', 'vout2', 'signal2', 'enable2', 'vout3', 'signal3', 'enable3']]
            
            self.update_props(data=data, vout=(data['vout1'].median(), data['vout2'].median()))
            return True
        else:
            raise ValueError(
                'Input file {name} not recognized.'.format(name=fname))

    def find_header_text(self, fname, search_string):
        "identify the end of file header based on looking for a unique string"
        with open(fname, 'r', encoding="utf8", errors='ignore') as f:
            pos = 0
            cur_line = f.readline()
            stripped = re.sub(r'\s', '', cur_line)
            while not stripped.startswith(search_string):
                if f.tell() == pos:
                    return False
                pos = f.tell()
                cur_line = f.readline()
                stripped = re.sub(r'\s', '', cur_line)
                        

        f.close()
        if pos < os.path.getsize(fname):
            return True

        return False
