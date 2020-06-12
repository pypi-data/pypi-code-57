from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from networktools.environment import get_env_variable

data = dict(user=get_env_variable('COLLECTOR_DBUSER'),
            passw=get_env_variable('COLLECTOR_DBPASS'),
            dbname=get_env_variable('COLLECTOR_DBNAME'),
            hostname=get_env_variable('COLLECTOR_DBHOST'),
            port=get_env_variable('COLLECTOR_PORT'))


class CollectorSession:
    def __init__(self, *args, **kwargs):
        self.db_engine = 'postgresql://{user}:{passw}@{hostname}:{port}/{dbname}'.format(
            **kwargs)
        self.engine = create_engine(self.db_engine)
        self.connection = self.engine.connect()
        self.session = sessionmaker(bind=self.engine)()

    def get_session(self):
        return self.session


if __name__=='__main__':    
    csession = CollectorSession(**data)
    session = csession.get_session()
    engine = csession.engine
    connection = csession.connection
