#!/usr/bin/env python3

import rich
import blessed

from statistics import mean
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text
from rich.progress import (Progress,
                           BarColumn,
                           TimeRemainingColumn,
                           ProgressColumn)
from datetime import timedelta


class TimeElapsedColumn(ProgressColumn):
    """Renders estimated time elapsed."""

    # Only refresh twice a second to prevent jitter
    max_refresh = 0.5

    def render(self, task):
        """Show time elapsed."""
        elapsed = task.elapsed
        if elapsed is None:
            return Text("-:--:--", style="progress.percentage")
        remaining_delta = timedelta(seconds=int(elapsed))
        return Text(str(remaining_delta), style="progress.percentage")


class Dashboard(object):

    """docstring for Dashboard"""

    def __init__(self,
                 title='Dashboard',
                 interval=1,
                 show_parameters=True,
                 show_loggers=True,
                 show_progress=True,
                 history_length=1000,
                 ):
        super(Dashboard, self).__init__()
        self.title = title
        self.interval = interval
        self.show_parameters = show_parameters
        self.show_loggers = show_loggers
        self.show_progress = show_progress
        self.history_length = history_length
        self.key_values = {}
        self.loggers = {}
        self.reset()
        self._progress = None
        self.dashboard_height = 0
        self.print_line = 0
        self.print_buffer = []

    def parameter(self, key, value):
        """docstring for parameter"""
        self.key_values[key] = value
        self.history_append(key, ':', value)

    def parameters(self, dictionary):
        """docstring for parameters"""
        for key, value in dictionary.items():
            self.parameter(key, value)

    def log(self, key, value):
        """docstring for log"""
        if key not in self.loggers:
            self.loggers[key] = []
        self.loggers[key].append(value)
        self.history_append(key, ':', value)

    def history_append(self, *args, **kwargs):
        """appends to the history print buffer"""
        self.print_buffer.append((args, kwargs))
        self.print_buffer = self.print_buffer[-self.history_length:]

    def reset(self):
        """resets counting only, not logged values"""
        self._step = 0
        self._terminal = blessed.Terminal()

    def clear(self):
        """clear printable area only"""
        with self._terminal.location(0, self.dashboard_height):
            emptyline = ' ' * self._terminal.width
            for _ in range(self._terminal.height - self.dashboard_height - 1):
                rich.print(emptyline)

    def summary(self, pad=False):
        new_height = 0

        # Print title
        title = self.title
        title = rich.text.Text(title, justify='center', style='bright_green')
        rich.print(Panel(title, box=rich.box.HEAVY, style='bright_green'))
        print()
        new_height += 3

        # Print key-values
        if len(self.key_values) and self.show_parameters:
            kv_title = 'Parameters'
            kv_title = rich.text.Text(kv_title, style='yellow')
            kv_title = Rule(kv_title)
            rich.print(kv_title)
            new_height += 2
            kv_table = rich.table.Table(title=None,
                                        box=rich.box.MINIMAL_HEAVY_HEAD,
                                        style='bright_green',
                                        expand=True,
                                        header_style='cyan')
            kv_table.add_column('Name', justify='left')
            kv_table.add_column('Value', justify='left', style='yellow')
            for key, value in self.key_values.items():
                kv_table.add_row(key, str(value))
                new_height += 1
            rich.print(kv_table)
            new_height += 3

        # Print loggers
        if len(self.loggers) and self.show_loggers:
            loggers_title = 'Loggers'
            loggers_title = rich.text.Text(loggers_title, style='magenta')
            loggers_title = Rule(loggers_title)
            rich.print(loggers_title)
            new_height += 2
            loggers_table = rich.table.Table(title=None,
                                             box=rich.box.MINIMAL_HEAVY_HEAD,
                                             style='bright_green',
                                             expand=True,
                                             header_style='cyan')
            loggers_table.add_column('Name', justify='left')
            loggers_table.add_column('Mean @ ' + str(self.interval),
                                     justify='left',
                                     style='magenta')
            for key, values in self.loggers.items():
                value = str(mean(values[-self.interval:]))
                loggers_table.add_row(key, value)
                new_height += 1
            rich.print(loggers_table)
            new_height += 3

        # Print progress bar
        if self._progress is not None and self.show_progress:
            if self._step > 0:
                self._progress.update(self._task,
                                      advance=self.interval,
                                      visible=True)
            self._progress.refresh()
            rich.print('\n')
            new_height += 2

        # Print rule
        step = rich.text.Text('Step ' + str(self._step), style='cyan')
        step = Rule(step)
        rich.print(step)
        new_height += 2

        # Set new height and clean screen
        self.dashboard_height = new_height
        self.print_line = new_height
        if pad:
            self.clear()

    def step(self):
        """docstring for step"""
        if self._step % self.interval == 0:
            with self._terminal.location(0, 0):
                self.summary(pad=True)

        # Mark in print buffer
        self.history_append('\n--- Step ' + str(self._step) + ' ---', )

        # Increment the step
        self._step += 1

    def print(self, *args, **kwargs):
        num_newlines = args.count('\n') + 1
        if self.print_line + num_newlines >= self._terminal.height:
            self.clear()
            self.print_line = self.dashboard_height
        with self._terminal.location(0, self.print_line):
            rich.print(*args, **kwargs)
        self.history_append(*args, **kwargs)
        self.print_line += num_newlines

    def __call__(self, iterator):
        """docstring for __call__"""
        self.iterator = iterator
        total_length = len(iterator)
        self._progress = Progress(
            '[progress.description]{task.description}',
            '[progress.percentage]{task.percentage:>3.0f}%',
            BarColumn(),
            TimeElapsedColumn(),
            '[green]•',
            TimeRemainingColumn(),
            auto_refresh=False,
        )
        self._task = self._progress.add_task(
            description='[cyan] Progress',
            total=total_length,
            visible=False,
        )
        return self

    def __iter__(self):
        """docstring for __iter__"""
        self.reset()
        with self._terminal.fullscreen():
            for res in self.iterator:
                self.step()
                yield res
        for args, kwargs in self.print_buffer:
            rich.print(*args, **kwargs)
