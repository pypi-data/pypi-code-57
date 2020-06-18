import logging

from celery.result import AsyncResult

from api.model.ResultVO import ResultVO, FAIL_CODE
from cloudcelery import celery
from schedule import TriggerActor
from munch import Munch
import json

log = logging.getLogger('Ficus')


@celery.task(name='tasks.on_request', bind=True, max_retries=2, default_retry_delay=1 * 6)
def on_request(self, protocol):
    """
    从celery接收协议
    :param self:
    :param protocol:
    :return:
    """
    log.info(f"从celery中获取到任务:{protocol}")
    try:
        # 子进程中也开启eureka_client的刷新,因为celery也会起子进程,所以只能在这里初始化了
        from py_eureka_client import eureka_client
        import config
        eureka_client.init_discovery_client(eureka_server=config.eureka_default_zone, renewal_interval_in_secs=4)
    except:
        pass

    body = Munch(json.loads(protocol))

    result: ResultVO = TriggerActor.handle_trigger(body, True)  # ResultVO

    if result.code == FAIL_CODE:
        # 让celery的任务也置失败
        raise RuntimeError(result.msg)

    return {'status': True, 'data': result.to_dict()}
