from utils.orm.src.database import connect
from utils.orm.src.management import create_tables, drop_tables


class PostgresqlService:

    def __init__(self, host):
        self.db = connect('argus', host, 5432, 'argus', 'panoptes')

    def setup(self):
        create_tables(self.db)

    def clean(self):
        drop_tables(self.db)
