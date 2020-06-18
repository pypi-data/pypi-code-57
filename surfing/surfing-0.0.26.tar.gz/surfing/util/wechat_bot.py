import datetime
import requests
import json
import time
from .config import SurfingConfigurator

class WechatBot(object):

    def __init__(self):
        self.wechat_webhook = SurfingConfigurator().get_wechat_webhook_settings('wechat_webhook')

    def send(self, markdown_content):
        # Send markdown content
        message = {
            'msgtype': 'markdown',
            'markdown': {
                'content': markdown_content
            }
        }
        res = requests.post(url=self.wechat_webhook, data=json.dumps(message), timeout=20)

    def send_data_update_status(self, dt, failed_tasks, updated_count):
        # Send markdown content
        markdown_content = f'{dt} 已完成数据更新，'
        if len(failed_tasks) == 0:
            markdown_content += '所有数据更新成功'
        else:
            markdown_content += '以下数据更新失败: '
            for key, task_names in failed_tasks.items():
                if len(task_names) > 0:
                    markdown_content += f'\n>{key}: <font color=\"error\">{task_names}</font>'

        markdown_content += '\n更新数据统计: '
        for key, item_count in updated_count.items():
            for item, count in item_count.items():
                markdown_content += f'\n>{key}.{item}: <font color=\"info\">{count}</font>'

        print(markdown_content)
        return self.send(markdown_content)
