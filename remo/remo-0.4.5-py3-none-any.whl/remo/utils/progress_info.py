from datetime import datetime, timedelta


class ProgressInfo:
    hundred_percent = 100

    def __init__(self, total: int, items: str = 'items', text: str = ''):
        self.total = total
        self.count = 0
        self.start = datetime.now()
        self.reported = -1
        self.items = items
        self.text = text

    def report(self, count: int = 1, **kwargs):
        self.count += count

        percentage = int(self.count / self.total * self.hundred_percent)
        if percentage > self.reported:
            self._report(percentage, **kwargs)

    def _report(self, percentage: int, **kwargs):
        elapsed = (datetime.now() - self.start).seconds + 1e-3
        avg_speed = self.count / elapsed
        eta = timedelta(seconds=int((self.total - self.count) / avg_speed))
        self.reported = percentage

        timestamp = datetime.now().strftime("%H:%M:%S")
        text = f' {self.text}: ' if self.text else ' '
        msg = (f'[{timestamp} RemoApp] INFO -{text}Progress: {percentage}% ({self.count}/{self.total}).')
               # f'elapsed {timedelta(seconds=int(elapsed))} - speed: {"%.2f" % avg_speed} {self.items}/s')
        if eta and not self.is_done():
            msg = f'{msg} ETA: {eta}'
        else:
            msg = f'{msg}                '

        # if kwargs:
        #     msg = f'{msg} {kwargs}'
        self._print(msg)

    def is_done(self):
        return self.reported == self.hundred_percent

    def _print(self, text):
        end = '\n' if self.is_done() else '\r'
        print(text, end=end)
