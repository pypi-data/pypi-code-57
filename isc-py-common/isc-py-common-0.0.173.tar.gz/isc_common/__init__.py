import logging
import os
from logging import Logger
from threading import Lock

from django.conf import settings

logger1 = logging.getLogger(__name__)


def dictinct_list(l, _sorted=False, key=None):
    ds = []
    for item in l:
        if not item in ds:
            ds.append(item)

    if _sorted:
        return sorted(ds, key=lambda x: x[key])
    return ds


def setAttr(o, name, value):
    o[name] = value
    return o


def delAttr(o, name):
    if name in o:
        del o[name]
        return True
    else:
        return False


def isEmptyDict(dictionary):
    for element in dictionary:
        if element:
            return True
        return False


def delete_drive_leter(path):
    path = path.replace(os.path.sep, os.path.altsep)
    if path.find(':') != -1:
        path = (path.split(':')[1]).replace(os.path.sep, os.path.altsep)
        path = ''.join(path)

    if path.startswith(os.altsep):
        return path[1:]
    return path


def get_drive_leter(path):
    path = path.replace(os.path.sep, os.path.altsep)
    if path.find(':') != -1:
        return f"{(path.split(':')[0])}:"
    return None


def replace_alt_set(path):
    return path.replace(os.altsep, os.sep).replace(f'{os.sep}{os.sep}', os.sep)


def replace_sep(path):
    return path.replace(os.sep, os.altsep)


def del_last_not_digit(str):
    res = ''
    flag = False
    for ch in reversed(str):
        if flag or ch.isdigit():
            res += ch
            flag = True

    return res[::-1]


def str_to_bool(s):
    if s in ['True', 'true']:
        return True
    elif s in ['False', 'false']:
        return False
    else:
        raise ValueError(f'{s} is not a good boolean string')


def bool_to_jsBool(value):
    if value == True:
        return "true"
    return "false"


class StackElementNotExist(Exception):
    def __init__(self, *args, **kwargs):  # real signature unknown
        super().__init__('Соответствие не найдено.')


class MultipleStackElement(Exception):
    def __init__(self, *args, **kwargs):  # real signature unknown
        super().__init__('Не однозначный выбор.')


def cleanProgresses(id_progresses=None, exclude_processes=None):
    from isc_common.models.deleted_progresses import Deleted_progresses
    from isc_common.models.progresses import Progresses

    if settings.LOCKS.locked('cleanProgresses'):
        return

    settings.LOCKS.acquire('cleanProgresses')
    try:
        if isinstance(id_progresses, str):
            _id_progresses = []
            _id_progresses.append(id_progresses)
            id_progresses = _id_progresses

        if isinstance(exclude_processes, str):
            _exclude_processes = []
            _exclude_processes.append(exclude_processes)
            exclude_processes = _exclude_processes

        if isinstance(id_progresses, list):
            for process in Progresses.objects.filter():
                for p in id_progresses:
                    if str(process.id_progress).find(p) != -1:
                        if isinstance(exclude_processes, list):
                            exc = False
                            for ep in exclude_processes:
                                if str(process.id_progress).find(ep) != -1:
                                    exc = True
                                    break
                            if not exc:
                                Progresses.objects.filter(id=process.id).delete()
                        else:
                            Progresses.objects.filter(id=process.id).delete()

            for process in Deleted_progresses.objects.filter():
                for p in id_progresses:
                    if str(process.id_progress).find(p) != -1:
                        if isinstance(exclude_processes, list):
                            exc = False
                            for ep in exclude_processes:
                                if str(process.id_progress).find(ep) != -1:
                                    exc = True
                                    break
                            if not exc:
                                Deleted_progresses.objects.filter(id=process.id).delete()
                        else:
                            Deleted_progresses.objects.filter(id=process.id).delete()
        else:
            if isinstance(exclude_processes, list):
                for process in Progresses.objects.filter():
                    if isinstance(exclude_processes, list):
                        exc = False
                        for ep in exclude_processes:
                            if str(process.id_progress).find(ep) != -1:
                                exc = True
                                break
                        if not exc:
                            Progresses.objects.filter(id=process.id).delete()
                    else:
                        Progresses.objects.filter(id=process.id).delete()

                for process in Deleted_progresses.objects.filter():
                    if isinstance(exclude_processes, list):
                        exc = False
                        for ep in exclude_processes:
                            if str(process.id_progress).find(ep) != -1:
                                exc = True
                                break
                        if not exc:
                            Deleted_progresses.objects.filter(id=process.id).delete()
                    else:
                        Deleted_progresses.objects.filter(id=process.id).delete()
            else:
                Progresses.objects.filter().delete()
                Deleted_progresses.objects.filter().delete()
        settings.LOCKS.release('cleanProgresses')
    except:
        settings.LOCKS.release('cleanProgresses')


class Stack:

    def __iter__(self):
        return self.stack.__iter__()

    def __init__(self, stack=[]):
        self.stack = stack.copy()

    def top(self, index=1):
        if len(self.stack) < index:
            return None
        return self.stack[len(self.stack) - index]

    def pop(self):
        if len(self.stack) < 1:
            return None
        return self.stack.pop()

    def push(self, item, exists_function=None, logger=None):
        if callable(exists_function):
            if exists_function(item) == False:
                self.stack.append(item)
                if isinstance(logger, Logger):
                    logger.debug(f'self.stack.append: {item}')
            else:
                if isinstance(logger, Logger):
                    logger.debug(f'self.stack.not append: {item}')
                return False
        else:
            self.stack.append(item)
            if isinstance(logger, Logger):
                logger.debug(f'self.stack.append: {item}')

        if isinstance(logger, Logger):
            logger.debug(f'size stack: {len(self.stack)}')
        return True

    def size(self):
        return len(self.stack)

    def copy(self):
        return Stack(self.stack)

    def find(self, function):
        return [item for item in self.stack if function(item)]

    def exists(self, function):
        return len([item for item in self.stack if function(item)]) > 0

    def find_one(self, function):
        res = self.find(function=function)
        if len(res) == 0:
            raise StackElementNotExist()
        elif len(res) > 1:
            raise MultipleStackElement()

        return res[0]

    def __str__(self):
        return "\n" + ', '.join([str(item.id) for item in self.stack])


class StackLocs(Stack):
    def acquire(self, id):
        try:
            id, lock = self.find_one(lambda x: x[0] == id)
        except StackElementNotExist:
            lock = Lock()
            self.push((id, lock))
        lock.acquire()
        logger1.debug(f'lock.acquire() ID: {id}')

    def locked(self, id):
        try:
            id, lock = self.find_one(lambda x: x[0] == id)
            return lock.locked()
        except StackElementNotExist:
            return False

    def release(self, id):
        try:
            id, lock = self.find_one(lambda x: x[0] == id)
            if lock.locked():
                lock.release()
                logger1.debug(f'lock.release() ID: {id}')
        except StackElementNotExist:
            pass


def get_list_nums_key_dict(data):
    res = []
    if isinstance(data, dict):
        if data.get('0'):
            idx = 0
            while True:
                _data = data.get(str(idx))
                if isinstance(_data, dict):
                    res.append(_data)
                else:
                    break
                idx += 1
        else:
            res.append(data)
    return res
