from zunzun import Config
from injector import singleton, inject
from sqlalchemy import create_engine


@singleton
class Engine:
    @inject
    def __init__(self, config: Config):
        self.config = config
        self._engine = create_engine(self.config.DB_CONFIG, echo=True)

    def __call__(self):
        return self._engine
