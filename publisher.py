from dataclasses import dataclass, field

from session import MQSession
from enums import MQTopic


@dataclass
class MQPublisher:
    """
    Class that implements RabbitMQ publish method.
    """
    topic: MQTopic
    _session: MQSession = field(default_factory=MQSession.default_session)

    def publish(self, body: dict) -> None:
        """
        Publish a message into RabbitMQ queue.
        :param body: Body of the message
        """
        with self._session as session:
            channel = session.channel()
            channel.exchange_declare(
                exchange="rabbitmq", exchange_type="topic")
            channel.basic_publish(
                exchange="rabbitmq",
                routing_key=self.topic.value,
                body=body)
