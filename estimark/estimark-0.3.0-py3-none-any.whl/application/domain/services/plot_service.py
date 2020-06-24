import json
import logging
from typing import Dict, List
from abc import ABC, abstractmethod
from ..models import Schedule, Slot, Task
from ..repositories import SlotRepository


logger = logging.getLogger(__name__)


class PlotService(ABC):
    @abstractmethod
    def plot_gantt(self, schedule: Schedule) -> str:
        "Plot gantt method to be implemented."

    @abstractmethod
    def plot_kanban(self, tasks: List[Task], sort: List[str] = None,
                    group: str = None) -> str:
        "Plot kanban method to be implemented."


class MemoryPlotService(PlotService):
    def __init__(self) -> None:
        self.gantt_plotted = False
        self.kanban_plotted = False

    def plot_gantt(self, schedule: Schedule) -> None:
        self.gantt_plotted = True
        logging.info(f"MEMORY PLOT. SCHEDULE: {schedule.name}")

    def plot_kanban(self, tasks: List[Task], sort: List[str] = None,
                    group: str = None) -> None:
        self.kanban_plotted = True
        logging.info(f"MEMORY KANBAN PLOT. TASKS #: {len(tasks)}")
