from ..core.common import Config
from ..application.domain.repositories import SlotRepository
from ..core.plot import AltairPlotService
from .base_factory import BaseFactory


class AltairFactory(BaseFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.config = config
        self.plot_dir = self.config.get('plot_dir', '.')

    def altair_plot_service(self, slot_repository: SlotRepository,
                            ) -> AltairPlotService:
        plot_service = AltairPlotService(
            self.plot_dir, slot_repository)
        return plot_service
