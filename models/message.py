
from models.message_types import MessageTypes

class Message(object):
    def __init__(self, type: MessageTypes, val, src):
        """
        Initialize a Package object.

        Args:
            type (MessageTypes): The type of the message.
            val: The value of the message.
            src: The source of the message.
        """
        # Assign the type of the message
        self.type = type

        # Assign the value of the message
        self.val = val

        # Assign the source of the message
        self.src = src
