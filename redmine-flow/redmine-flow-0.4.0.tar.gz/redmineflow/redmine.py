import redminelib
import keyring

def connect():
    redmine = redminelib.Redmine('https://redmine.isdc.unige.ch/', 
                       username=keyring.get_password('redmine', 'username'), 
                       password=keyring.get_password('redmine', 'password'))
    return redmine

