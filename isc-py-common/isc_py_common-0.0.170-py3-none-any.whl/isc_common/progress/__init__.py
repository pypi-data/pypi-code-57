import logging
import sys
import traceback
from contextlib import contextmanager

from django.conf import settings
from django.utils import timezone
from tqdm import tqdm

from isc_common.bit import IsBitOff
from isc_common.models.deleted_progresses import Deleted_progresses
from isc_common.models.progresses import Progresses
from isc_common.ws.progressStack import ProgressStack

logger = logging.getLogger(__name__)

progress_deleted = 'Прогресс удален.'

class ProgressDroped(Exception):
    ...


@contextmanager
def managed_progress(qty, user, id, message='Обработано позиций', title='Обработано позиций', props=0):
    progress = Progress(id=id, qty=qty, user=user, message=message, title=title, props=props)
    try:
        yield progress
        progress.close()
    except ProgressDroped as ex:
        progress.close()
        if callable(progress.except_func):
            progress.except_func()
        Deleted_progresses.objects.filter(id_progress=id, user=user).delete()
        raise ex
    except Exception as ex:
        exc_info = sys.exc_info()
        stackTrace = traceback.format_exception(*exc_info)
        stackTrace = '<br>'.join(stackTrace)
        stackTrace = f'<pre>{stackTrace}</pre>'
        del exc_info
        progress.sendError(message=str(ex), stackTrace=stackTrace)
        if callable(progress.except_func):
            progress.except_func()
        progress.close()
        raise ex


class Progress:
    progress = None
    pbar = None
    except_func = None
    enable_ws_progress = None

    def __init__(self, user, id, qty=0, message='Обработано позиций', title='Обработано позиций', label_contents=None, props=0):
        from isc_common.auth.models.user import User

        self.message = message
        self.title = title
        self.props = props
        self.id = id
        self.enable_ws_progress = IsBitOff(self.props, 1)

        if self.enable_ws_progress == True:
            if isinstance(user, int):
                self.user = User.objects.get(id=user)
            elif isinstance(user, User):
                self.user = user
            else:
                raise Exception(f'user must be User instance or User_id.')

        self.qty = qty

        if self.enable_ws_progress == False:
            self.pbar = tqdm(total=qty)
        else:
            # if self.qty > 0:
            channel = f'common_{self.user.username}'
            self.progress = ProgressStack(
                host=settings.WS_HOST,
                port=settings.WS_PORT,
                channel=channel,
                props=self.props,
                user_id=self.user.id
            )

            self.demand_str = f'<h3>{self.message}</h3>'

            # if not self.check_exists():

            deleted, _ = Deleted_progresses.objects.filter(id_progress=self.id, user=self.user).delete()
            logger.debug(f'Deleted_progresses: {deleted}')

            self.progress.show(
                cntAll=qty,
                id=self.id,
                label_contents=label_contents if label_contents else self.demand_str,
                title=f'<b>{title}</b>',
            )

            # if IsBitOff(props, 1):
            self.progresses, created = Progresses.objects.get_or_create(
                id_progress=self.id,
                user=self.user,
                defaults=dict(
                    cnt=0,
                    label_contents=self.demand_str,
                    qty=self.qty,
                    message=self.message,
                    props=self.props,
                    title=self.title,
                    lastmodified=timezone.now()
                )
            )

        self.cnt = 0

    def check_exists(self):
        return Progresses.objects.filter(id_progress=self.id, user=self.user).count() > 0

    def step(self):
        from isc_common.models.deleted_progresses import Deleted_progresses

        res = 0
        if self.enable_ws_progress == True:
            if self.progress != None:
                self.progress.setCntDone(self.cnt, self.id)
                self.cnt += 1
                if self.qty == self.cnt:
                    self.cnt = 0
                self.progresses.cnt = self.cnt
                self.progresses.lastmodified = timezone.now()
                self.progresses.save()
                deleted_count = Deleted_progresses.objects.filter(id_progress=self.id, user=self.user).count()
                return deleted_count
        else:
            self.pbar.update()
            logger.debug(str(self.pbar))
        return res

    def setContentsLabel(self, content):
        if self.progress != None:
            self.progress.setContentsLabel(labelContents=content, id=self.id)
            self.progresses.label_contents = content
            self.progresses.save()

    def setQty(self, qty):
        if self.progress != None:
            self.progress.setCntAll(cntAll=qty, id=self.id)
            self.progresses.qty = qty
            self.progresses.save()

    def sendInfo(self, message):
        if self.progress != None:
            self.progress.sendInfo(message=message)

    def sendWarn(self, message):
        if self.progress != None:
            self.progress.sendWarn(message=message)

    def sendError(self, message, stackTrace=None):
        if self.progress != None:
            self.progress.sendError(message=message, stackTrace=stackTrace)

    def sendMessage(self, type, message=None):
        if self.progress != None:
            self.progress.sendMessage(type=type, message=message)

    def close(self):
        if self.progress != None:
            self.progress.close(self.id)
            try:
                self.progresses.delete()
            except AssertionError:
                pass

        if self.pbar:
            self.pbar.close()
