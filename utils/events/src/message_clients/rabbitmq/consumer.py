class Consumer:

    def __init__(self, client, queue, on_message_callback):
        self.client = client
        self.queue = queue
        self.on_message_callback = on_message_callback

    def start(self):
        with self.client.channel() as channel:
            channel.basic_consume(queue=self.queue, on_message_callback=self._process_message)
            channel.start_consuming()

    def close(self):
        self.client.close()

    def _process_message(self, channel, method, _props, body):
        next_message = self.on_message_callback(body)
        channel.basic_ack(delivery_tag=method.delivery_tag)

        if not next_message:
            channel.stop_consuming()
