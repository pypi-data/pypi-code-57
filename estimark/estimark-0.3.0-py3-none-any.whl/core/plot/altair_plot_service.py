
import altair as alt
import pandas as pd
import logging
from typing import List
from datetime import date
from pathlib import Path
from collections import Counter
from ...application.domain.models import Schedule, Task
from ...application.domain.repositories import SlotRepository
from ...application.domain.services import PlotService


logger = logging.getLogger(__name__)


class AltairPlotService(PlotService):
    def __init__(self, plot_dir: str,
                 slot_repository: SlotRepository) -> None:
        self.slot_repository = slot_repository
        self.plot_dir = plot_dir

    def plot_gantt(self, schedule: Schedule) -> None:
        logging.info(f"ALTAIR PLOT SCHEDULE: {schedule.name}")
        slots = self.slot_repository.search(
            [('schedule_id', '=', schedule.id)])
        slot_dict_list = [vars(slot) for slot in slots]
        state = f"| State: <{schedule.state}> " if schedule.state else ""
        title = f"{schedule.name} {state}| {date.today()}"

        source = pd.DataFrame(slot_dict_list)
        chart = alt.Chart(source).mark_bar().encode(
            x='start',
            x2='end',
            y='name'
        ).properties(title=title)

        output_file = str(Path(self.plot_dir).joinpath('gantt.html'))

        chart.save(output_file)

    def plot_kanban(self, tasks: List[Task],
                    sort: List[str] = None, group: str = None) -> None:
        logging.info(f"ALTAIR KANBAN PLOT. TASKS #: {len(tasks)}")
        group = group or 'state'
        detail = 'owner' if group == 'state' else 'state'

        task_dict_list = [{'weight': 1, **vars(task)}
                          for task in tasks if not task.summary]

        counts = Counter(task_dict[group] for task_dict
                         in task_dict_list).most_common()
        _, max_depth = next(iter(counts))

        source = pd.DataFrame(task_dict_list)

        title = f"Kanban Chart | {date.today()}"
        block_height = 50
        block_width = block_height * 8

        base = alt.Chart(source).mark_bar(
            color='black'
        ).encode(
            x=alt.X(group, axis=alt.Axis(
                orient='top', labelAngle=0, labelFontSize=15), sort=sort),
            y=alt.Y('sum(weight)', sort='descending', stack='zero'),
            order=alt.Order('id',  sort='ascending')
        ).properties(
            title=title,
            width=block_width * len(counts),
            height=block_height * max_depth)

        bars = base.encode(
            color=alt.Color('id:N', legend=None))

        text = base.mark_text(
            dy=-(block_height * 0.33),
            color='black'
        ).encode(
            text='name')

        info = base.mark_text(
            dy=-(block_height * 0.67),
            dx=(block_width * 0.3),
            color='#2F4F4F'
        ).encode(
            text=detail)

        chart = bars + text + info

        output_file = str(Path(self.plot_dir).joinpath('kanban.html'))

        chart.save(output_file)
