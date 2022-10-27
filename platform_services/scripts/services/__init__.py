from .minio import MinioService
from .postgresql import PostgresqlService
from .rabbitmq import RabbitMQService


services = [
    MinioService(),
    RabbitMQService(),
    PostgresqlService()
]
