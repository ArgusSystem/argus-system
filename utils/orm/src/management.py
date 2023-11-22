from peewee import Model
from utils.orm.src import View


def create_tables(database):
    assert database.is_connection_usable()
    database.create_tables(Model.__subclasses__())


def drop_tables(database):
    assert database.is_connection_usable()
    database.drop_tables(Model.__subclasses__(), cascade=True)


def create_views(database):
    assert database.is_connection_usable()
    for view_class in View.__subclasses__():
        database.execute_sql(view_class.create_view_str())


def drop_views(database):
    assert database.is_connection_usable()
    for view_class in View.__subclasses__():
        database.execute_sql(view_class.drop_view_str())
