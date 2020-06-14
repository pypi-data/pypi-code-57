import datetime
import string

from pter.searcher import get_relative_date
from pytodotxt import Task


DATETIME_FMT = '%Y-%m-%d-%H-%M-%S'


def duration_as_str(duration):
    seconds = int(duration.total_seconds())
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    
    result = ''
    if hours > 0:
        result += f'{hours}h'
    if minutes > 0:
        result += f'{minutes}m'

    return result


def parse_duration(text):
    duration = datetime.timedelta(0)

    sign = 1
    if text.startswith('-'):
        sign = -1
        text = text[1:]
    elif text.startswith('+'):
        text = text[1:]

    value = ''
    for char in text.lower():
        if char in string.digits:
            value += char
        elif char == 'h' and len(value) > 0:
            duration += datetime.timedelta(hours=int(value))
            value = ''
        elif char == 'm' and len(value) > 0:
            duration += datetime.timedelta(minutes=int(value))
            value = ''
        elif char == 's' and len(value) > 0:
            duration += datetime.timedelta(seconds=int(value))
            value = ''
        elif char == 'd' and len(value) > 0:
            duration += datetime.timedelta(days=int(value))
            value = ''
        elif char == 'w' and len(value) > 0:
            duration += datetime.timedelta(days=int(value)*7)
            value = ''
        else:
            # parse error
            return None

    if len(value) > 0:
        duration += datetime.timedelta(minutes=int(value))
    
    duration *= sign

    return duration


def dehumanize_dates(text, tags=None):
    """Replace occurrences of relative dates in tags"""
    if tags is None:
        tags = ['due', 't']

    offset = 0
    found_any = True

    while found_any and offset < len(text):
        found_any = False
        for match in Task.KEYVALUE_RE.finditer(text, offset):
            if match is None:
                offset = len(text)
                break
            found_any = True
            if match.group(2) in tags and not Task.DATE_RE.match(match.group(3)):
                then = get_relative_date(match.group(3))
                if then is not None:
                    then = then.strftime(Task.DATE_FMT)
                    text = text[:match.start(3)] + \
                           then + \
                           text[match.end(3):]
                    offset = match.start(3) + len(then)
                    break
            offset = match.end(3) + 1
    return text


def ensure_up_to_date(source, task):
    ok = True
    if source.refresh():
        ok = False
        source.parse()
        tasks = [other for other in source.tasks if other.raw.strip() == task.raw.strip()]
        if len(tasks) > 0:
            ok = True
            task = tasks[0]

    if ok:
        return task

    return None


def toggle_tracking(task):
    if 'tracking' in task.attributes:
        return update_spent(task)
    task.add_attribute('tracking', datetime.datetime.now().strftime(DATETIME_FMT))
    return True


def update_spent(task):
    attrs = task.attributes
    now = datetime.datetime.now()
    tracking = attrs.get('tracking', None)
    raw_spent = attrs.get('spent', None)

    if tracking is None:
        return False

    try:
        then = datetime.datetime.strptime(tracking[0], DATETIME_FMT)
    except ValueError:
        return False

    if raw_spent is not None:
        spent = parse_duration(raw_spent[0])
        if spent is None:
            self.status_bar.addstr(0, 0, "Failed to parse 'spent' time", self.color(Window.ERROR))
            self.status_bar.noutrefresh()
            return False
    else:
        spent = datetime.timedelta(0)
    
    diff = now - then
    if diff <= datetime.timedelta(minutes=1):
        diff = datetime.timedelta(0)

    task.remove_attribute('tracking', tracking[0])

    # TODO: make the minimal duration configurable
    if diff >= datetime.timedelta(minutes=1):
        spent = duration_as_str(spent + diff)
        if raw_spent is None:
            task.add_attribute('spent', spent)
        else:
            task.replace_attribute('spent', raw_spent[0], spent)

        return True

    return False

