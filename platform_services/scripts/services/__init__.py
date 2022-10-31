from .minio import MinioService
from .postgresql import PostgresqlService
from .rabbitmq import RabbitMQService

host = 'localhost'

services = [
    MinioService(host),
    RabbitMQService(host),
    PostgresqlService(host)
]
