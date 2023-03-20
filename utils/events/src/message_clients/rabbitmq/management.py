from pika.exceptions import ChannelClosedByBroker


def setup_exchange(channel, name, durable=True):
    channel.exchange_declare(name, durable=durable)


def delete_exchange(channel, name):
    channel.exchange_delete(name)


def setup_queue(channel, name, durable=True):
    channel.queue_declare(name, durable=durable)


def delete_queue(channel, name):
    channel.queue_delete(name)


def queue_bind(channel, queue_name, exchange_name, routing_key):
    channel.queue_bind(queue_name, exchange_name, routing_key)


def queue_exists(channel, queue_name):
    try:
        channel.queue_declare(queue_name, passive=True)
        return True
    except ChannelClosedByBroker:
        return False


def queue_unbind(channel, queue_name, exchange_name, routing_key):
    channel.queue_unbind(queue_name, exchange_name, routing_key)


def queue_purge(channel, queue_name):
    channel.queue_purge(queue_name)
