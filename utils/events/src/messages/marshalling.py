from .message_type import MessageType

from fastavro import parse_schema, schemaless_reader, schemaless_writer
from io import BytesIO
import os.path as path
import json


RESOURCES_DIR = '../../resources'


class Marshaller:

    def __init__(self, message_type):
        filepath = path.join(path.dirname(__file__), RESOURCES_DIR, message_type.id + '.json')

        with open(filepath, 'r') as file:
            self.schema = parse_schema(json.load(file))

        self.message_class = message_type.message_class

    def encode(self, record):
        buffer = BytesIO()
        schemaless_writer(buffer, self.schema, record)
        buffer.seek(0)
        return buffer

    def decode(self, record):
        return self.message_class(**schemaless_reader(record, self.schema))


schemas = {}

for mtype in MessageType:
    schemas[mtype] = Marshaller(mtype)

def encode(message_type, message):
    return schemas[message_type].encode(message.to_json())


def decode(message_type, record):
    return schemas[message_type].decode(record)
