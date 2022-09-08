import datetime
import decimal

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from . import settings


def alchemy_encoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
        
# DatabaseManager uses SQLAlchemy ORM
class DatabaseManager(object):
    #static vars for global use
    db_engine = None 
    DBSession = None
    Base = declarative_base()
    DB_CONNECTION = {
        'db_host': settings.DB_HOST,
        'db_port': settings.DB_PORT,
        'db_name': settings.DB_NAME,
        'db_username': settings.DB_USERNAME,
        'db_password': settings.DB_PASSWORD,
    }

    @staticmethod
    def get_database():
        if (DatabaseManager.db_engine is None):
            print("Initializing database connection DB_CONNECTION: " + DatabaseManager.DB_CONNECTION['db_host'] + " " + DatabaseManager.DB_CONNECTION['db_name'])
            echoAllSQL = False #os.getenv('DFD_ENV') == 'dev'
            DatabaseManager.db_engine = create_engine(
                DatabaseManager.get_conn_string(),
                pool_size=10,
                max_overflow=5,
                connect_args={"sslmode": "allow", "connect_timeout": 30, "options": "-c timezone=utc"},
                echo=echoAllSQL,
            )
            # TODO research how expire_on_commit=False effects db connection pool at scale
            DatabaseManager.DBSession = sessionmaker(bind=DatabaseManager.db_engine, expire_on_commit=False)
            DatabaseManager.DBSession.configure(bind=DatabaseManager.db_engine)
            DatabaseManager.Base.metadata.bind = DatabaseManager.db_engine
            DatabaseManager.Base.metadata.create_all(DatabaseManager.db_engine)
            return DatabaseManager.db_engine
        else:
            return DatabaseManager.db_engine

    @classmethod
    def get_conn_string(cls):
        return "postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}".format(**cls.DB_CONNECTION)

    @classmethod
    def get_conn_string_with_adapter(cls):
        return "postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}".format(
            **cls.DB_CONNECTION
        )
    
    @staticmethod
    def get_db_session() -> Session:
        if DatabaseManager.DBSession is None:
            DatabaseManager.get_database()

        if DatabaseManager.DBSession is not None:
            return DatabaseManager.DBSession()
        else:
            print("Error no database connection established, skipping get db session.")
            
        return None

    @staticmethod
    def get_db_conn():
        return DatabaseManager.get_database().connect()

    @staticmethod
    def get_db_base():
        DatabaseManager.get_database()
        return DatabaseManager.Base




