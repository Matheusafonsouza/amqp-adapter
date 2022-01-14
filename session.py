from __future__ import annotations
import pika
from pika.adapters.blocking_connection import BlockingConnection
from os import environ


class MQSession:
    """
    Class that implement AMQP protocol comunication.
    """

    def __init__(self, host, port, username, password, virtual_host):
        """
        Class constructor.
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.virtual_host = virtual_host

    def __enter__(self) -> BlockingConnection:
        """
        Create a connection at RabbitMQ.
        :returns: Connection session
        """
        credentials = pika.PlainCredentials(self.username, self.password)
        params = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=credentials,
            virtual_host=self.virtual_host)

        # pylint: disable=attribute-defined-outside-init
        self.connection = pika.BlockingConnection(params)
        return self.connection

    def __exit__(self, exc_type, exc_value, exc_tb):
        """
        Stop the RabbitMMQ connection.
        """
        self.connection.close()

    @classmethod
    def default_session(cls) -> MQSession:
        """
        A default session for RabbitMQ protocol, with all connection data.
        :returns: MQSession instance
        """
        return MQSession(
            host=environ.get("MQ_HOST", "rabbitmq"),
            port=environ.get("MQ_PORT", 5672),
            username=environ.get("MQ_USER", "brock"),
            password=environ.get("MQ_PASS", "onix"),
            virtual_host=environ.get("MQ_PORT", "pewtergym"),
        )