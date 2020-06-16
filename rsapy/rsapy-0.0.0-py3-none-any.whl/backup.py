import pickle
import os

backup = os.path.join(os.path.dirname(__file__), 'backup').rstrip(os.sep)
backup += os.sep

def set_backup(data, user, filename):
    userid = '-'.join([str(ord(x)) for x in user])
    open(backup+'backup-'+userid+'-'+filename+'.dat', 'wb').write(
        pickle.dumps(data))

def get_backup(user, filename):
    userid = '-'.join([str(ord(x)) for x in user])
    return pickle.loads(open(backup+'backup-'+userid+'-'+filename+'.dat',
                             'rb').read())

def del_backup(user, filename):
    userid = '-'.join([str(ord(x)) for x in user])
    os.remove(backup+'backup-'+userid+'-'+filename+'.dat')
