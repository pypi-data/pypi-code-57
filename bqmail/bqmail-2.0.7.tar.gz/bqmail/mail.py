from bqmail.query import Query
from obspy import UTCDateTime
from obspy.taup import TauPyModel
from obspy.clients.iris import Client
import smtplib
import time
from email.mime.text import MIMEText
model = TauPyModel()
cld = Client()


def sendmail(sender, contents, server='localhost',
             recipient='breq_fast@iris.washington.edu',
             port=465, password=''):
    msg = MIMEText(contents, 'text')
    msg['Subject'] = 'BREQ_fast'
    msg['From'] = 'bqmail<'+sender+'>'
    msg['To'] = recipient
    if server == 'localhost':
        try:
            smtpObj = smtplib.SMTP(server)
            smtpObj.sendmail(sender, recipient, msg.as_string())
            return True
        except smtplib.SMTPException:
            print("Error when send mail by localhost")
            return False
    else:
        try:
            smtpObj = smtplib.SMTP_SSL(server, port)
            smtpObj.login(sender, password)
            smtpObj.sendmail(sender, recipient, msg.as_string())
            return True
        except smtplib.SMTPException:
            print("Error in linking {}".format(server))
            return False


def generatemsg(username, inst, mailname, media):
    msg = ''
    msg += '.NAME '+username+'\n'
    msg += '.INST '+inst+'\n'
    msg += '.MAIL\n'
    msg += '.EMAIL '+mailname+'\n'
    msg += '.PHONE\n'
    msg += '.FAX\n'
    msg += '.MEDIA '+media+'\n'
    msg += '.ALTERNATE MEDIA '+media+'\n'
    msg += '.ALTERNATE MEDIA '+media+'\n'
    return msg


class BQMail():
    def __init__(self, mailname, username='bqmail',
                 inst='', media='Electronic (FTP)',
                 server='localhost', password=''):
        self.query = Query()
        self.mailname = mailname
        self.server = server
        self.password = password
        self.username = username
        self.inst = inst
        self.media = media
        self.msgs = []
        self.labels = []
        self.header = generatemsg(username, inst, mailname, media)

    def query_stations(self, **kwargs):
        self.query.get_stations(**kwargs)

    def query_events(self, **kwargs):
        self.query.get_events(**kwargs)

    def send_mail(self, arrange='station', time_sleep=2, **kwargs):
        if arrange == 'station':
            self.station_mail(**kwargs)
        elif arrange == 'continue':
            self.conti_mail(**kwargs)
        else:
            raise ValueError('variable arrange must be in \'station\' and \'continue\'')
        for label, msg in zip(self.labels, self.msgs):
            succ = sendmail(self.mailname, msg, server=self.server,
                            password=self.password)
            if succ:
                print('successfully send {}'.format(label))
                time.sleep(time_sleep)
            # with open('msg.{}'.format(label), 'w') as f:
            #     f.write(msg)

    def conti_mail(self, starttime=UTCDateTime(2000, 1, 1),
                   endtime=UTCDateTime.now(), time_val_in_hours=24,
                   channel='BH?', location=''):
        self.query.get_conti(starttime, endtime, hours=time_val_in_hours)
        for sdt, edt in self.query.conti_time:
            label = sdt.strftime('%Y.%m.%d')
            self.labels.append(label)
            msg = self.header
            msg += '.LABEL {}\n.END\n'.format(label)
            for net in self.query.stations:
                for sta in net:
                    msg += '{} {} {} {} 1 {} {}\n'.format(
                            sta.code, net.code, sdt.strftime('%Y %m %d %H %M %S'), 
                            edt.strftime('%Y %m %d %H %M %S'), channel, location)
            self.msgs.append(msg)

    def station_mail(self, time_before=0, time_after=1000,
                     mark='o', channel='BH?', location=''):
        for net in self.query.stations:
            for sta in net:
                msg = self.header
                label = '{}.{}'.format(net.code, sta.code)
                self.labels.append(label)
                msg += '.LABEL {}\n.END\n'.format(label)
                if mark == 'o':
                    for i, evt in self.query.events.iterrows():
                        b_time = (evt['date'] + time_before).strftime('%Y %m %d %H %M %S')
                        e_time = (evt['date'] + time_after).strftime('%Y %m %d %H %M %S')
                        msg += '{} {} {} {} 1 {} {}\n'.format(
                                sta.code, net.code, b_time, e_time,
                                channel, location)
                else:
                    for i, evt in self.query.events.iterrows():
                        ttime = self.get_ttime(evt, sta, phase=mark)
                        if ttime is None:
                            continue
                        else:
                            b_time = (evt['date'] + ttime + time_before).strftime('%Y %m %d %H %M %S')
                            e_time = (evt['date'] + ttime + time_after).strftime('%Y %m %d %H %M %S')
                            msg += '{} {} {} {} 1 {} {}\n'.format(
                                    sta.code, net.code, b_time, e_time,
                                    channel, location)
                self.msgs.append(msg)

    def get_ttime(self, evt, obspy_station, phase='P'):
        da = cld.distaz(obspy_station.latitude, obspy_station.longitude,
                        evt.evla, evt.evlo)
        arr = model.get_travel_times(evt.evdp, da['distance'], phase_list=[phase])
        if len(arr) == 0:
            return None
        else:
            return arr[0].time

