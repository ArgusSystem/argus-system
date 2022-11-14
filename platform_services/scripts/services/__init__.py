from .minio import MinioService
from .postgresql import PostgresqlService
from .rabbitmq import RabbitMQService

host = 'argus'

services = [
    MinioService(host),
    RabbitMQService(host),
    PostgresqlService(host)
]
