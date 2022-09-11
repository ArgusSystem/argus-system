from fastavro import parse_schema, schemaless_reader, schemaless_writer
from io import BytesIO
import os.path as path
import json


RESOURCES_DIR = path.join(path.dirname(__file__), '../../resources')


class Marshaller:

    def __init__(self, message_type, message_class):
        with open(path.join(RESOURCES_DIR, message_type.value + '.json'), 'r') as file:
            self.schema = parse_schema(json.load(file))

        self.message_class = message_class


    def encode(self, record):
        buffer = BytesIO()
        schemaless_writer(buffer, self.schema, record)
        buffer.seek(0)
        return buffer

    def decode(self, record):
        return self.message_class(**schemaless_reader(record, self.schema))