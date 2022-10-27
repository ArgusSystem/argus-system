from peewee import Model


def create_tables(database):
    assert database.is_connection_usable()
    database.create_tables(Model.__subclasses__())


def drop_tables(database):
    assert database.is_connection_usable()
    database.drop_tables(Model.__subclasses__())
