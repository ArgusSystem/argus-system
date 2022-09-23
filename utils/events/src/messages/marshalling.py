from fastavro import parse_schema, schemaless_reader, schemaless_writer
from io import BytesIO
import os.path as path
import json

RESOURCES_DIR = path.join(path.dirname(__file__), '..', '..', 'resources')

schema_cache = {}


def encode(message):
    schema = _get_message_schema(type(message))
    buffer = BytesIO()
    schemaless_writer(buffer, schema, message.to_json())
    buffer.seek(0)
    return buffer.read()


def decode(message_class, record):
    schema = _get_message_schema(message_class)
    return message_class(**schemaless_reader(BytesIO(record), schema))


def _get_message_schema(message_class):
    if message_class not in schema_cache:
        with open(path.join(RESOURCES_DIR, message_class.__name__ + '.json'), 'r') as file:
            schema_cache[message_class] = parse_schema(json.load(file))

    return schema_cache[message_class]
