from concurrent.futures import ThreadPoolExecutor as __Pool__
from multiprocessing import cpu_count as __cpu__
from time import sleep
from os import system


def __checkpoint__(filename: str, save: bool = True, data: int = 0):
    open(filename, 'a').close()
    with open(filename, 'w' if save else 'r') as f:
        if save:
            f.write(str(
                max(data, 0)
            ))
        else:
            try:
                data = int(f.read() or 0)
            except: pass
    return data


def __write__(info, location):
    if info:
        with open(location, 'a') as f:
            for item in info:
                f.write(str(item))
    return []


def __visual__(items, keys=False):
    keys = keys or ["", "~", "+", "-"]
    system('cls || clear')
    print(*[f'{keys[i%len(keys)]}{items[i]}' for i in range(len(items))], sep='\t')


class Batch:
    def __init__(
            self,
            data,
            rate: int = __cpu__(),
            scale: int = 0,
            interval: float = 1,
            output: str = '_output.txt',
            write: callable = __write__,
            progress: str = '_progress.txt',
            checkpoint: callable = __checkpoint__,
            visual: callable = __visual__
    ):
        copy = list(data)  # greater startup time, but still better then using a list
        if isinstance(data, enumerate):
            data = enumerate([x[1] for x in copy])
        else:
            data = copy
        self.total = len(copy)
        self.valid = 0
        self.invalid = 0
        self.workers = 0

        self.data = {'in': data, 'out': []}
        self.rate = int(max(rate, 2))
        self.scale = int(max(scale or self.rate, 2))
        self.interval = interval
        self.output = output
        self.write = write
        self.progress = progress
        self.checkpoint = checkpoint
        self.visual = visual

        del copy, data, rate, scale, interval, output, write, progress, checkpoint, visual  # free memory of duplicates
        self.pool = __Pool__(max_workers=self.rate)

    def start(self, fn):
        progress = self.checkpoint(self.progress, save=False)

        def wrapper(args):  # yes I know, the lack of '*' is intentional
            try:
                value = args[0](*args[1:])
            except Exception as e:
                print(e)
                value = False
            if value:
                self.valid += 1
                self.data['out'].append(value)
            else:
                self.invalid += 1
            self.workers -= 1

        def combo():
            self.data['out'] = self.write(self.data['out'], self.output)
            self.checkpoint(self.progress, save=True, data=progress + self.valid + self.invalid)
            self.visual([
                f'{max(progress + self.valid + self.invalid, 0)}/{self.total}',
                self.workers,
                self.valid,
                self.invalid
            ])

        try:
            for index, item in self.data['in']:
                if index < progress:
                    continue  # skip

                if index % (self.rate * self.scale):
                    sleep(self.interval)  # disperse time
                else:
                    while self.workers > self.rate:  # wait until queue is acceptable
                        combo()
                        sleep(self.interval * self.rate)
                    combo()

                self.workers += 1
                self.pool.submit(wrapper, (fn, index, item))

            self.pool.shutdown(wait=True)
        except:
            try: self.pool.shutdown(wait='n' not in f'{input("finish (Y/n): ")}'.lower())
            except: pass
        combo()

        try: combo()
        except: pass
        combo()

    def help(self):
        _self_ = '\n\t'.join(['%s=%s'% (k, vars(self)[k]) for k in vars(self)])
        print(f"""
data: enumerate,
rate: int = cpu_count(),
scale: int = 0,
interval: float = 1,
output: str = '_output.txt',
write: callable = __write__,
progress: str = '_progress.txt',
checkpoint: callable = __checkpoint__,
visual: callable = __visual__
If you need more help, then look at the source code here: https://github.com/ritzKraka/batchelor.py/
self:
    {_self_}
        """)
