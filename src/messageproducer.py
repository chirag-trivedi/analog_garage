import queue
import time
import random
import logging
import string
from typing import Tuple


class MessageProducer:
    def __init__(self, num_messages: int) -> None:
        """
        Initializes the MessageProducer and the messages queue.

        Parameters:
            num_messages (int): The total number of messages to be produced by this instance.
        """
        self.logger = logging.getLogger("Producer")
        self.num_messages: int = num_messages
        self.messages = queue.Queue()

    def produce_messages(self) -> None:
        """
        Generates and queues a set number of random messages with phone numbers.

        Returns:
            None
        """
        for _ in range(self.num_messages):
            phone_number, message = self.create_message()
            try:
                self.messages.put((phone_number, message))
                time.sleep(0.01)
            except Exception as e:
                self.logger.exception(f"Exception in putting messages to the queue {e}")

    def create_message(self) -> Tuple[str, str]:
        """
        Creates a single message with a randomly generated phone number and content.

        Returns:
            Tuple[str, str]: A tuple containing the generated phone number and message content.
        """
        phone_number = self.get_random_phone_number()
        message = self.get_random_message()
        return phone_number, message

    @staticmethod
    def get_random_phone_number() -> str:
        """
        Generates a random US phone number in the format '+1XXXXXXXXXX'.

        Returns:
            str: A string representing a randomly generated phone number.
        """
        return f"+1{random.randint(1000000000, 9999999999)}"

    @staticmethod
    def get_random_message() -> str:
        """
        Generates a random message containing alphanumeric characters with a random length up to 100 letters + digits.

        Returns:
            str: A randomly generated message string.
        """
        length = random.randint(1, 100)
        msg = "".join(random.choices(string.ascii_letters + string.digits, k=length))
        return msg
