import pandas as pd
from psense_common import PSenseParser
from psense_common.psense_parser import is_float
import unittest
from unittest.mock import (patch, MagicMock, Mock)
from datetime import (datetime, timedelta)
import pytz

def is_dst ():
    """Determine whether or not Daylight Savings Time (DST)
    is currently in effect"""

    x = datetime(datetime.now().year, 1, 1, 0, 0, 0, tzinfo=pytz.timezone('US/Eastern')) # Jan 1 of this year
    y = datetime.now(pytz.timezone('US/Eastern'))

    # if DST is in effect, their offsets will be different
    return not (y.utcoffset() == x.utcoffset())

class TestPSenseParser(unittest.TestCase):
    def setUp(self):
        self.parser = PSenseParser(debugmode=True)
        pass

    def test_is_float(self):
        self.assertTrue(is_float(0))
        self.assertTrue(is_float('0'))
        self.assertTrue(is_float('0.5'))
        self.assertFalse(is_float('A'))
        self.assertFalse(is_float({'value': 0.5}))
        self.assertFalse(is_float([0.5]))

    def test_force_source(self):
        self.assertRaises(IOError, self.parser.force_source, 'not-a-real-data-type')
        type1 = 'PSHIELD'
        self.parser.force_source(type1)
        self.assertEqual(self.parser.source, type1)
        self.assertEqual(self.parser.we_count, self.parser.num_channels[type1])
        type2 = 'BWII-DL'
        self.parser.force_source(type2)
        self.assertEqual(self.parser.source, type2)
        self.assertEqual(self.parser.we_count, self.parser.num_channels[type2])

    def test_find_header_text(self):
        mock_type = 'PSHIELD'
        search_string = self.parser.header_text[mock_type]

        m_open = MagicMock()
        m_methods = Mock()
        m_methods.tell.side_effect = [1, 2, 3, 4, 5, 15, 15]
        m_methods.readline.side_effect = ['random', 'random', search_string, 'random', 'random', 'random']
        m_open().__enter__.return_value = m_methods

        with patch('builtins.open', m_open, create=True):
            with patch('os.path.getsize', return_value=11):
                self.assertTrue(self.parser.find_header_text('fake_file', search_string))
                self.assertFalse(self.parser.find_header_text('fake_file', 'string-that-doesnt-exist'))

    def test_identify_file_source(self):

        self.assertRaises(FileNotFoundError, self.parser.identify_file_source, 'fake_file')

        self.parser.identify_file_source(fpath='tests/pshield_example')
        self.assertEqual(self.parser.source, 'PSHIELD')
        self.assertEqual(self.parser.we_count, self.parser.num_channels['PSHIELD'])
        self.parser.identify_file_source(fpath='tests/gamry_example')
        self.assertEqual(self.parser.source, 'EXPLAIN')
        self.parser.identify_file_source('tests/__init__.py')
        self.assertEqual(self.parser.source, None)

    def test_parse_record(self):
        starting_time = datetime.now()

        self.parser.force_source('BWII-MINI')
        data = ','.join([starting_time.isoformat(), 'sensor_record', '10', '1.0', '1000', '500', '1', '0', '2.0', '1010', '1', '0', '3.0', '1500', '1', '0', '3300'])
        res = self.parser.parse_record(data)
        self.assertTrue(datetime.fromisoformat(res[0]) - starting_time < timedelta(seconds=3))
        self.assertEqual(res[1], [.5, .51, 1.0])
        self.assertEqual(res[2], [1.0, 2.0, 3.0])
        self.assertEqual(res[3], [True, True, True])
        data = ','.join([starting_time.isoformat(), 'sensor_record', '10', '1.0', '1000', '500', '0', '0', '2.0', '1010', '0', '0', '3.0', '1500', '0', '0', '3300'])
        res = self.parser.parse_record(data)
        self.assertEqual(res[3], [False, False, False])

        self.parser.force_source('BWII-DL')
        data = ','.join([starting_time.isoformat(), 'sensor_record', '1', '1', '.2', '.1', '0', '1', '0', '10', '.4', '.2', '.1', '1', '0', '0', '3260'])
        res = self.parser.parse_record(data)
        self.assertTrue(datetime.fromisoformat(res[0]) - starting_time < timedelta(seconds=3))
        self.assertEqual(res[1], [0.0001, 0.0002])
        self.assertEqual(res[2], [1.0, 10.0])
        self.assertEqual(res[3], [True, True])
        data = ','.join([starting_time.isoformat(), 'sensor_record', '1', '1', '.2', '.1', '0', '-1', '0', '10', '.4', '.2', '.1', '0', '0', '0', '3260'])
        res = self.parser.parse_record(data)
        self.assertEqual(res[3], [False, False])

        data = '1, 1554417874.0000026, 12.51'
        self.parser.force_source('PSHIELD')
        res = self.parser.parse_record(data)
        if is_dst():
            self.assertEqual(res[0], '2019-04-04T15:44:34.000003')  # local time, not utc
        else: 
            self.assertEqual(res[0], '2019-04-04T14:44:34.000003')  # local time, not utc
        self.assertTrue(res[1] is None)
        self.assertEqual(res[2], 12.51)
        self.assertTrue(res[3])

        data = '0.399550	7.3E-9'
        self.parser.force_source('VFP')
        res = self.parser.parse_record(data)
        self.assertTrue(datetime.fromisoformat(res[0]) - starting_time < timedelta(seconds=3))
        self.assertTrue(res[1] == 0.39955)
        self.assertTrue(res[2] == 7.3)
        self.assertTrue(res[3])

        data = '2015-12-26 20:19:18,0.72,0.3,0.72'
        self.parser.force_source('WEB1CHAN')
        res = self.parser.parse_record(data)
        self.assertEqual(res[0], '2015-12-26T20:19:18')
        self.assertEqual(res[1], 0.3)
        self.assertEqual(res[2], 0.72)
        self.assertTrue(res[3])

        data = '2019-07-09 12:13:14,9.59,0.502,19.21,0.403,9.59,15.7'
        self.parser.force_source('WEB2CHAN')
        res = self.parser.parse_record(data)
        self.assertEqual(res[0], '2019-07-09T12:13:14')
        self.assertEqual(res[1], [.502, 0.403])
        self.assertEqual(res[2], [9.59, 19.21])
        self.assertEqual(res[3], [True, True])

    def test_load_no_source(self):
        testfile = 'tests/pshield_example'
        
        # fake source
        self.parser.source = 'fake-source'
        self.assertRaises(ValueError, self.parser.load_rawfile, testfile, None, None)

    def test_load_pshield(self):
        testfile = 'tests/pshield_example'
        # pshield file
        self.parser.identify_file_source(testfile)
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data
        self.assertEqual(df['vout1'].iloc[-1], .5)
        self.assertEqual(df['signal1'].iloc[-1], 5.29)
        if is_dst():
            self.assertEqual(df['timestamp'].iloc[-1], pd.Timestamp('2018-07-23 17:28:08.229594946'))
        else:
            self.assertEqual(df['timestamp'].iloc[-1], pd.Timestamp('2018-07-23 16:28:08.229594946'))

    def test_load_bwii_script(self):
        # psense format (bwii-instrument.py)
        testfile = 'tests/psense_example'
        self.parser.identify_file_source(testfile)
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data
        self.assertEqual(df['vout1'].iloc[-1], 0)
        self.assertEqual(df['signal1'].iloc[-1], 1)
        self.assertEqual(df['vout2'].iloc[-1], 2)
        self.assertEqual(df['signal2'].iloc[-1], 3)
        self.assertEqual(df['timestamp'].iloc[-1], pd.Timestamp('2019-03-04T13:08:54'))

        self.assertTrue(df['enable1'].iloc[-1])
        self.assertTrue(df['enable2'].iloc[0])

    def test_load_bwii_dl(self):
        # bwii format (bwii-dl)
        testfile = 'tests/bwii_example'
        self.parser.identify_file_source(testfile)
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data
        self.assertEqual(df['vout1'].iloc[-1], 0.487)
        self.assertEqual(df['signal1'].iloc[-1], 1.76)
        self.assertEqual(df['vout2'].iloc[-1], 0)
        self.assertEqual(df['signal2'].iloc[-1], 0)
        self.assertEqual(df['timestamp'].iloc[-1], pd.Timestamp('2019-03-04 16:37:42'))

        start_time = '2019/01/01 12:00'
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, False))
        df = self.parser.data
        self.assertEqual(df['vout1'].iloc[-1], 0.487)
        self.assertEqual(df['signal1'].iloc[-1], 1.76)
        self.assertEqual(df['vout2'].iloc[-1], 0)
        self.assertEqual(df['signal2'].iloc[-1], 0)
        self.assertEqual(df['timestamp'].iloc[-1], pd.Timestamp('2019-01-01 12:05:00'))

        self.assertTrue(self.parser.load_rawfile(testfile, start_time, True))
        df = self.parser.data
        self.assertEqual(df['vout1'].iloc[-1], 0.487)
        self.assertEqual(df['signal1'].iloc[-1], 1.76)
        self.assertEqual(df['vout2'].iloc[-1], 0)
        self.assertEqual(df['signal2'].iloc[-1], 0)
        self.assertEqual(df['timestamp'].iloc[-1], pd.Timestamp('2019-01-01 12:00:00'))

    def test_load_bwii_mini(self):
        testfile = 'tests/bwii_mini_example'
        self.parser.identify_file_source(testfile)
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data
        self.assertEqual(df['vout1'].iloc[1], 0.501)
        self.assertEqual(df['signal1'].iloc[1], .175)
        self.assertEqual(df['vout2'].iloc[1], 0.502)
        self.assertEqual(df['signal2'].iloc[1], 1.75)
        self.assertEqual(df['vout3'].iloc[1], 1)
        self.assertEqual(df['signal3'].iloc[1], 17.5)
        
        self.assertEqual(df['vout1'].iloc[-1], 0.501)
        self.assertEqual(df['signal1'].iloc[-1], 175)
        self.assertEqual(df['vout2'].iloc[-1], -0.488)
        self.assertEqual(df['signal2'].iloc[-1], 0)
        self.assertEqual(df['vout3'].iloc[-1], -0.488)
        self.assertEqual(df['signal3'].iloc[-1], 0)
        self.assertEqual(df['timestamp'].iloc[-1], pd.Timestamp('2020-01-01 19:32:17'))

        start_time = '2019/01/01 12:00'
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, False))
        df = self.parser.data
        self.assertEqual(df['timestamp'].iloc[-1], pd.Timestamp('2019-01-01 12:07:00'))

        self.assertTrue(self.parser.load_rawfile(testfile, start_time, True))
        df = self.parser.data
        
        self.assertEqual(df['timestamp'].iloc[-1], pd.Timestamp('2019-01-01 12:00:00'))

    def test_load_bwii_util(self):
        # files downloaded from BWII_Util.exe have extra whitespace. Make sure they are loaded properly
        testfile = 'tests/bwii_util_example'
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, 'BWII-MINI')
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data
        self.assertEqual(len(df.index), 20)

    def test_load_webapp_v1v2(self):
        # web app file
        testfile = 'tests/web1chan_example'
        self.parser.identify_file_source(testfile)
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data
        self.assertEqual(df['vout1'].iloc[-1], .3)
        self.assertEqual(df['signal1'].iloc[-1], 2.77)
        self.assertTrue(df['enable1'].iloc[-1])

        self.assertEqual(df['timestamp'].iloc[-1], pd.Timestamp('2019-07-26 17:12:30'))
        

        testfile = 'tests/web2chan_example'
        self.parser.identify_file_source(testfile)
        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data
        self.assertEqual(df['vout1'].iloc[-1], .5)
        self.assertEqual(df['signal1'].iloc[-1], 5)
        self.assertTrue(df['enable1'].iloc[-1])

        self.assertEqual(df['vout2'].iloc[-1], .4)
        self.assertEqual(df['signal2'].iloc[-1], 15)
        self.assertTrue(df['enable2'].iloc[-1])

        self.assertEqual(df['timestamp'].iloc[-1], pd.Timestamp('2019-07-09 17:35:24'))
        
        testfile = 'tests/web3chan_example'
        self.parser.identify_file_source(testfile)
        self.assertEqual(self.parser.source, 'WEB3CHAN')
        self.assertEqual(self.parser.we_count, 3)

        self.assertTrue(self.parser.load_rawfile(testfile, None, None))
        df = self.parser.data

        self.assertEqual(df['vout1'].iloc[-1], 0.508)
        self.assertEqual(df['signal1'].iloc[-1], 2.48)
        self.assertTrue(df['enable1'].iloc[-1])

        self.assertEqual(df['vout2'].iloc[-1], -0.501)
        self.assertEqual(df['signal2'].iloc[-1], 0.03)
        self.assertTrue(df['enable2'].iloc[-1])

        self.assertEqual(df['timestamp'].iloc[-1], pd.Timestamp('2020-02-10 11:04:54'))
        
    def test_load_vfp600(self):
        # vfp600
        start_time = '2019/01/01 12:00'
        testfile = 'tests/vfp_example'
        self.parser.identify_file_source(testfile)
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, False))
        df = self.parser.data
        self.assertEqual(df['timestamp'].iloc[0], pd.Timestamp(start_time))
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, True))
        df = self.parser.data
        self.assertTrue(df['timestamp'].iloc[0] < pd.Timestamp(start_time))
        ts = [df['timestamp'].iloc[-1], pd.Timestamp(start_time)]
        self.assertTrue(pd.Timedelta(max(ts) - min(ts)).seconds < 1)
        
        self.assertEqual(df['vout1'].iloc[-1], 0.39955)
        self.assertEqual(round(df['signal1'].iloc[-1],2), 3.8)
        self.assertTrue(df['enable1'].iloc[-1])

        # vfp600 #2
        start_time = '2019/01/01 12:00'
        testfile = 'tests/vfp_example2'
        self.parser.identify_file_source(testfile)
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, False))
        df = self.parser.data
        self.assertEqual(df['timestamp'].iloc[0], pd.Timestamp(start_time))
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, True))
        df = self.parser.data
        self.assertTrue(df['timestamp'].iloc[0] < pd.Timestamp(start_time))
        ts = [df['timestamp'].iloc[-1], pd.Timestamp(start_time)]
        self.assertTrue(pd.Timedelta(max(ts) - min(ts)).seconds < 1)

        self.assertEqual(df['vout1'].iloc[-2], 0.101215)
        self.assertEqual(round(df['signal1'].iloc[-2],2), 0.19)
        self.assertEqual(df['vout1'].iloc[-1], 0.101219)
        self.assertEqual(round(df['signal1'].iloc[-1],3), 0.244)
        self.assertTrue(df['enable1'].iloc[-1])

    def test_load_explain(self):
        # gamry explain
        start_time = '2018/09/11 12:00'
        testfile = 'tests/gamry_example'
        self.parser.identify_file_source(testfile)
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, False))
        df = self.parser.data
        self.assertEqual(df['timestamp'].iloc[0], pd.Timestamp(start_time))
        self.assertTrue(self.parser.load_rawfile(testfile, start_time, True))
        df = self.parser.data
        self.assertEqual(df['timestamp'].iloc[0], pd.Timestamp(start_time))

        self.assertEqual(df['vout1'].iloc[-1], 0.499654)
        self.assertEqual(df['signal1'].iloc[-1], 3.60525)
        self.assertTrue(df['enable1'].iloc[-1])