import re

from remo_app.remo.api.constants import TaskType

separators = re.compile(r'[\s_-]+')


def parse_annotation_task(task: str) -> TaskType:
    if not task:
        return None

    if type(task) != str:
        return None

    task = separators.sub(' ', task).capitalize()
    try:
        return TaskType(task)
    except ValueError:
        return None
