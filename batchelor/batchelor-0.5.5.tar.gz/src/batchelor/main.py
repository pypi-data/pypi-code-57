import argparse
from concurrent.futures import ThreadPoolExecutor as __Pool__
from multiprocessing import cpu_count as __cpu__
from os import path, system
import sys
from time import sleep


'''
set presets
'''

presets = {
    'fast': [
        __cpu__() ** 2,
        0,
        0.5
    ],
    'medium': [
        int(__cpu__() ** 1.5),
        0,
        0.75
    ],
    'default': [
        __cpu__(),
        0,
        1
    ],
    'slow': [
        int(__cpu__() / 2),
        2,
        2
    ]
}
__save_name__ = path.basename(sys.argv[0]).split('.')[0]
default = [
    f'd_{__save_name__}.txt',
    *presets['default'],
    f'o_{__save_name__}.txt',
    f'p_{__save_name__}.txt'
]


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
            except:
                pass
    return data


def __write__(info, location):
    if info:
        with open(location, 'a') as f:
            for item in info:
                f.write(str(item))
    return []


def __visual__(items, keys=("", "~", "+", "-")):
    system('cls || clear')
    print(*[f'{keys[i%len(keys)]}{items[i]}' for i in range(len(items))], sep='\t')


class Batch:
    def __init__(
            self,
            data: list,
            rate: int = __cpu__(),
            scale: int = 0,
            interval: float = 1,
            output: str = '_output.txt',
            progress: str = '_progress.txt',
            write: callable = __write__,
            checkpoint: callable = __checkpoint__,
            visual: callable = __visual__
    ):
        data = list(data)  # greater startup time, but still better then using only a list
        self.total = len(data)
        self.valid = 0
        self.invalid = 0
        self.workers = 0

        self.data = {'in': enumerate(data), 'out': []}
        self.rate = int(max(rate, 2))
        self.scale = int(max(scale or self.rate, 2))
        self.interval = interval
        self.output = output
        self.progress = progress
        self.write = write
        self.checkpoint = checkpoint
        self.visual = visual

        del data, rate, scale, interval, output, progress, write, checkpoint, visual  # free memory of duplicates
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

                if item:  # check for falsy
                    self.workers += 1
                    self.pool.submit(wrapper, (fn, index, item))
                else:
                    self.invalid += 1

            self.pool.shutdown(wait=True)
        except:
            try:
                self.pool.shutdown(wait='n' not in f'{input("finish (Y/n) ")}'.lower())
            except:
                pass
        combo()

        try:
            combo()
        except:
            pass
        combo()

    def help(self):
        print(f'''
data: enumerate
    enumerable object to run through
rate: int (batchelor.__cpu__())
    how many workers to keep alive at once
scale: int (0)
    queue scale (0 == rate*rate)
interval: int (1)
    how fast to spawn new workers
output: str (dynamically chosen)
    filename to save results to (passed to write function)
progress: str (dynamically chosen)
    progress file (passed to checkpoint function)
write: function (batchelor.__write__)
    save(output)
checkpoint: function (batchelor.__checkpoint__)
    save/restore(save=True/False)
visual: function (batchelor.__visual__)  # x ~y +z -a
    visual status updates

NOTE: every function was made to be easily monkeypatched, so use it if you want.

If you need more help, then look at the source code here: https://github.com/ritzKraka/python-batchelor

{vars(self)}''')


'''
set production-ready functions
'''


def prompt():
    return {
        'rate': int(input(f'rate (?/{default[0]}) ') or default[1]),
        'scale': default[2],
        'interval': default[2],
        'output': input(f'output file (?/{default[3]}) ') or default[3],
        'progress': input(f'progress file (?/{defualt[4]}) ') or default[4],
    }


def launch(fn: callable, save=__save_name__, data=False, use_args=False):
    if use_args:
        args = argparse.ArgumentParser()
        args.add_argument('-d', '--data', type=argparse.FileType('r'), default=data or default[0])
        args.add_argument('-r', '--rate', type=int, default=default[1])
        args.add_argument('-s', '--scale', type=int, default=default[2])
        args.add_argument('-i', '--interval', type=int, default=default[3])
        args.add_argument('-o', '--output', type=str, default=default[4])
        args.add_argument('-p', '--progress', type=str, default=default[5])
        info = vars(args.parse_known_args()[0])
        del args
    else:
        info = {'data': data or argparse.FileType('r')(input(f'data file (?/{default[0]}) ') or default[0]), **prompt()}

    Batch(**info).start(fn)
