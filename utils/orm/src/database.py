from peewee import PostgresqlDatabase

db = PostgresqlDatabase(None)


def connect(database, host, port, user, password):
    db.init(database,
            host=host,
            port=port,
            user=user,
            password=password)

    db.connect()

    return db
