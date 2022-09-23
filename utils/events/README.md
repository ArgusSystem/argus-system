# Events module

The *events* module centralizes all the necessary components for an event-driven ecosystem, in particular to support the 
actor model, which is used in the distributed system. It features a client to connect to a message broker and 
produce/consume events in RabbitMQ and all messages are encoded/decoded using the _avro_ marshaller.


## Usage

### Producer

```python
from utils.events.src.message_clients.rabbitmq.publisher import Publisher
from utils.events.src.messages.video_chunk_message import VideoChunkMessage
from utils.events.src.messages.marshalling import encode

# Configuration for publisher
configuration = {
  'host': 'localhost',
  'username': 'user',
  'password': '1234',
  'exchange': 'argus',
  'routing_key': 'test'
}

# Create a publisher and a message to send
publisher = Publisher(configuration)
message = VideoChunkMessage('camera_id', 0)

# Encode message
encoded_message = encode(message)

# Send message to broker
publisher.publish(encoded_message)
```

### Consumer

```python
from utils.events.src.message_clients.rabbitmq.consumer import Consumer
from utils.events.src.messages.marshalling import decode
from utils.events.src.messages.video_chunk_message import VideoChunkMessage

# Configuration for consumer
configuration = {
  'host': 'localhost',
  'username': 'user',
  'password': '1234',
  'queue': 'video_chunks'
}

# Print every messaged received
def process_message(message):
    print(decode(VideoChunkMessage, message))
    return

# Create a consumer with a callback to handle messages
consumer = Consumer(configuration, process_message)

# Start consuming until the end of times
consumer.start()
```