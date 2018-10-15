from sqlalchemy import Table, Column, Integer, Float, String, BigInteger, DateTime, Boolean, Enum, Text, UniqueConstraint, MetaData
from sqlalchemy import create_engine
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy import inspect

import Config
import Schemas

class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DBHandler():
    __metaclass__ = Singleton

    engine = None
    session = None

    def __init__(self):
        self.initDB()

    def initDB(self):
        db_conf = Config.get_section('Database')
        user, password, host, name = db_conf['user'], db_conf['password'], db_conf['host'], db_conf['name']
        connection_string = 'postgresql://' + user + ':' + password + '@' + host + '/' + name

        self.engine = create_engine(connection_string, echo=False)
        self.session = sessionmaker(bind=self.engine)()
        self.metadata = MetaData(self.engine)

    def makeTable(self, name, schema):
        table = Table(name, self.metadata, *schema, extend_existing=True)
        table.create(checkfirst=True)
        return table
   
    def getTable(self, name):
        table = Table(name, self.metadata, autoload=True)
        return table

    def writeValue(self, sensor_id, sensor_type, sensor_value, sensor_time):
        schema = Schemas.types[sensor_type]['schema']
        table_name = sensor_id + '_' + sensor_type
        table = self.getOrCreateTable(table_name, schema)
        row = {'value': sensor_value, 'time': sensor_time}
        self.engine.execute(table.insert(), (row, ))

    def getOrCreateTable(self, name, schema, defaults=[]):
        iengine = inspect(self.engine)
        db_tables = iengine.get_table_names()
        is_new_table_created = False
        if name not in db_tables:
            print "Table is absent. Making table ...."
            self.makeTable(name, schema)
            is_new_table_created = True

        table = Table(name, self.metadata, autoload=True)
        db_columns = iengine.get_columns(name)
        db_column_names = [c["name"] for c in iengine.get_columns(name)]
        model_column_names = [c.name for c in schema if c.name is not None]
        if set(model_column_names) != set(db_column_names):
            print 'DB do not correspond Schema'
            self.session.close()
            table.drop(self.engine, checkfirst=False)
            self.engine.dispose()
            self.initDB()
            print iengine.get_table_names()
            table = self.makeTable(name, schema)
            is_new_table_created = True

        if defaults != [] and is_new_table_created:
            print defaults
            self.bulk_insert(table, defaults)

        return table

    def initialize(self, schema, sensor_id, sensor_type, defaults=[]):
        table_name = sensor_id + '_' + sensor_type
        table = self.getOrCreateTable(table_name, schema, defaults)
        return table

    def clear(self, params):
        pass

    def bulk_insert(self, table, insert_list):
        if len(insert_list) > 0:
            self.engine.execute(table.insert(), insert_list)

    def insert(self, table, row):
        self.engine.execute(table.insert(), (row,))

    def get_new_metadata(self):
        return MetaData(self.engine)

    def get_session(self):
        return self.session

    def get_engine(self):
        return self.engine

    def get_table_names(self):
        inspector = inspect(self.engine)
        return inspector.get_table_names()
