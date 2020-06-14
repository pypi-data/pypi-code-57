from zunzun import App
from injector import singleton
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .session import Session


class OrmApp(App):
    name = "orm"

    def register_services(self, injector):
        from .engine import Engine

        engine = injector.get(Engine)
        sess = sessionmaker(bind=engine(), class_=Session)
        injector.binder.bind(Session, to=sess(), scope=singleton)
