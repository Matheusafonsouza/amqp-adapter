from typing import Callable
from dataclasses import dataclass, field

from session import MQSession
from enums import MQTopic


@dataclass
class MQConsumer:
    """
    Class that implements RabbitMQ consumer method.
    """
    topic: MQTopic
    on_msg_cb: Callable[[dict], None]
    _session: MQSession = field(default_factory=MQSession.default_session)

    class Config:
        arbitrary_types_allowed = True

    def start(self):
        """
        Start RabbitMQ consumer for messages.
        """
        with self._session as session:
            channel = session.channel()
            channel.exchange_declare(
                exchange="rabbitmq", exchange_type="topic")
            result = channel.queue_declare("", exclusive=True)
            queue = result.method.queue
            channel.queue_bind(
                exchange="rabbitmq", queue=queue, routing_key=self.topic.value)
            channel.basic_consume(
                queue=queue,
                on_message_callback=self._on_message,
                auto_ack=True)
            channel.start_consuming()
