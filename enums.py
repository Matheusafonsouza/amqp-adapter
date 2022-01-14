from enum import Enum


class MQTopic(str, Enum):

    SCHEDULED = "debt.scheduled"
    SETTLED = "debt.settled"
    FAILED = "debt.failed"
