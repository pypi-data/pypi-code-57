#!/usr/bin/python
# coding: utf8

# Copyright 2019 Skiply
# 
from __future__ import unicode_literals

import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declared_attr, as_declarative

from sqlalchemy import Column, Integer

engine = None
db_session = None

def createDBEngine(uri):
	SQLALCHEMY_DATABASE_URI = uri

	engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False, pool_recycle=280, pool_size=10) # pool_size/overflow
	return engine

def createDBSessionManager(engine):
	db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
	return db_session

@as_declarative()
class SkiplyBase(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()