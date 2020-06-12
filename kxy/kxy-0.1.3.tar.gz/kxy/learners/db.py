
import os

from sqlalchemy import create_engine, event, exc, select
from sqlalchemy import Column, Text, Numeric, Integer
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from multiprocessing.util import register_after_fork


DB_USERNAME = 'postgres_root'
DB_PASSWORD = 'M7HozN3dS*1NxmoyU!I&'
DB_HOST = 'md-1.cqd3kdauu9s1.us-west-2.rds.amazonaws.com'
DB_PORT = '5432'
DB_NAME = 'kxy'
CONNECTION_URL = 'postgresql://{}:{}@{}:{}/{}'.format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
Base = declarative_base()

def preping_engine(engine):
	"""Add connection pre-pinging and multiprocessing guards.

	Every time a connection is
	Forces a connection to be reconnected if it is detected as having been shared to a sub-process.

	@see http://docs.sqlalchemy.org/en/rel_1_0/faq/connections.html#how-do-i-use-engines-connections-sessions-with-python-multiprocessing-or-os-fork
	@see http://docs.sqlalchemy.org/en/rel_1_1/core/pooling.html#pool-disconnects
	"""

	@event.listens_for(engine, "connect")
	def connect(dbapi_connection, connection_record):
		"""Record the pid creating each DB connection"""
		connection_record.info['pid'] = os.getpid()

	@event.listens_for(engine, "checkout")
	def checkout(dbapi_connection, connection_record, connection_proxy):
		"""Before handing over a connection from the pool, checks that it belongs to the current process and invalidates
		it if it doesn't causing a new connection to be created
		"""
		pid = os.getpid()
		if connection_record.info['pid'] != pid:
			# substitute log.debug() or similar here as desired
			logging.debug(
				"Parent process %(orig)s forked (%(newproc)s) with an open "
				"database connection, "
				"which is being discarded and recreated." %
				{"newproc": pid, "orig": connection_record.info['pid']})
			connection_record.connection = connection_proxy.connection = None
			raise exc.DisconnectionError(
				"Connection record belongs to pid %s, "
				"attempting to check out in pid %s" %
				(connection_record.info['pid'], pid)
			)

	@event.listens_for(engine, "engine_connect")
	def ping_connection(connection, branch):
		"""Pre-ping connection everytime we need it
			@see: http://docs.sqlalchemy.org/en/rel_1_1/core/pooling.html#pool-disconnects
			TODO: if/when we upgrade to SQLAlchemy 1.2, this can be replaced by a simple pool_pre_ping=True above
		"""
		if branch:
			# "branch" refers to a sub-connection of a connection,
			# we don't want to bother pinging on these.
			return

		# turn off "close with result".  This flag is only used with
		# "connectionless" execution, otherwise will be False in any case
		save_should_close_with_result = connection.should_close_with_result
		connection.should_close_with_result = False

		try:
			# run a SELECT 1.   use a core select() so that
			# the SELECT of a scalar value without a table is
			# appropriately formatted for the backend
			connection.scalar(select([1]))
		except exc.DBAPIError as err:
			# catch SQLAlchemy's DBAPIError, which is a wrapper
			# for the DBAPI's exception.  It includes a .connection_invalidated
			# attribute which specifies if this connection is a "disconnect"
			# condition, which is based on inspection of the original exception
			# by the dialect in use.
			if err.connection_invalidated:
				# run the same SELECT again - the connection will re-validate
				# itself and establish a new connection.  The disconnect detection
				# here also causes the whole connection pool to be invalidated
				# so that all stale connections are discarded.
				connection.scalar(select([1]))
			else:
				raise
		finally:
			# restore "close with result"
			connection.should_close_with_result = save_should_close_with_result

	return engine


def get_kxy_db_engine(**kwargs):
	"""
	Get an sqlalchemy database engine to the kxy database
	You can pass in overrides to the create_engine statement as keyword arguments
	Examples:
		To increase connection pool size and overflow limits:
		get_kxy_db_engine(pool_size=60, max_overflow=30)

		To debug sql queries sent to the db:
		get_kxy_db_engine(echo=True)
	"""
	engine = create_engine(CONNECTION_URL, **dict(echo=False, pool_recycle=600, **kwargs))
	register_after_fork(engine, engine.dispose)

	return preping_engine(engine)


class SpearmanCopulaDensityModel(Base):
	__tablename__ = 'max_ent_copula_densities'
	model_id_md5 = Column(Text, primary_key=True)
	model_id = Column(Text)
	created_at = Column(Numeric)
	max_entropy_constraints = Column(Text)
	d = Column(Integer, index=True)
	n_moments = Column(Integer, index=True)
	entropy = Column(Numeric, index=True)
	theta = Column(ARRAY(Numeric))
	n_constraints = Column(Integer, index=True)
	expectations = Column(ARRAY(Numeric))
	spearman_corr_matrix = Column(JSONB) 
	ordered_spearman_corr_matrix = Column(JSONB) 
	moment_constraints = Column(JSONB)


class CopulaEntropyModel(Base):
	__tablename__ = 'rv_copula_entropy_all'
	md5_corr = Column(Text, primary_key=True)
	ordered_spearman_corr_matrix = Column(JSONB)
	d = Column(Integer)
	count = Column(Integer)
	median_entropy = Column(Numeric)
	mean_entropy = Column(Numeric)
	min_entropy = Column(Numeric)
	max_entropy = Column(Numeric)
	entropy_std_err = Column(Numeric)



def get_session_factory():
    return scoped_session(sessionmaker(bind=get_kxy_db_engine()))


if __name__ == '__main__':
	Base.metadata.create_all(bind=get_kxy_db_engine(), checkfirst=True)

