from ..core.common import Config
from ..application.domain.common import QueryParser
from ..core.data.json import (
    init_json_database, JsonRepository,
    JsonClassificationRepository, JsonClassifierRepository,
    JsonLinkRepository, JsonScheduleRepository,
    JsonSlotRepository, JsonTaskRepository)
from .altair_factory import AltairFactory


class JsonFactory(AltairFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.config = config
        self.param_dir = self.config['param_dir']
        self.result_dir = self.config['result_dir']

    def json_classification_repository(self, query_parser: QueryParser,
                                       ) -> JsonClassificationRepository:
        repository = JsonClassificationRepository(
            self.param_dir, query_parser, file_suffix='param')
        return repository

    def json_classifier_repository(self, query_parser: QueryParser,
                                   ) -> JsonClassifierRepository:
        repository = JsonClassifierRepository(
            self.param_dir, query_parser, file_suffix='param')
        return repository

    def json_link_repository(self, query_parser: QueryParser,
                             ) -> JsonLinkRepository:
        repository = JsonLinkRepository(
            self.param_dir, query_parser, file_suffix='param')
        return repository

    def json_schedule_repository(self, query_parser: QueryParser,
                                 ) -> JsonScheduleRepository:
        repository = JsonScheduleRepository(
            self.result_dir, query_parser, file_suffix='result')
        return repository

    def json_slot_repository(self, query_parser: QueryParser,
                             ) -> JsonSlotRepository:
        repository = JsonSlotRepository(
            self.result_dir, query_parser, file_suffix='result')
        return repository

    def json_task_repository(self, query_parser: QueryParser,
                             ) -> JsonTaskRepository:
        repository = JsonTaskRepository(
            self.param_dir, query_parser, file_suffix='param')
        return repository
