from enum import Enum

"""
    Type of messages sent between nodes.
"""
class MessageTypes(Enum):
    HEARTBEAT = 'heartbeat'
    LAYER = 'layer'
    ACK = 'ack'
    REJECT = 'reject'
    ROUND = 'round'
    UPCAST = 'upcast'
