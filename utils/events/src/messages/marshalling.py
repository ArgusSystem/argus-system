from .message_type import MessageType

from fastavro import parse_schema, schemaless_reader, schemaless_writer
from io import BytesIO
import os.path as path


RESOURCES_DIR = '../../resources'


class Marshaller:

    def __init__(self, message_type):
        with open(path.join(RESOURCES_DIR, message_type.id + '.json'), 'r') as file:
            self.schema = parse_schema(file.read())

        self.message_class = message_type.message_class

    def encode(self, record):
        buffer = BytesIO()
        schemaless_writer(buffer, self.schema, record)
        buffer.seek(0)
        return buffer

    def decode(self, record):
        return schemaless_reader(record, self.schema)


schemas = {}

for mtype in MessageType:
    schemas[mtype.id] = Marshaller(mtype)

def encode(message_type, record):
    return schemas[message_type].encode(record)


def decode(message_type, record):
    return schemas[message_type].decode(record)
