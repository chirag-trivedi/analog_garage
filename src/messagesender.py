import threading
import queue
import random
import time


class MessageSender(threading.Thread):
    def __init__(
        self,
        message_queue: queue.Queue[tuple[str, str]],
        mean_processing_time: float,
        failure_rate: float,
    ) -> None:
        """
        Initializes the MessageSender with a message queue, processing time, and failure rate.

        Parameters:
            message_queue: The queue containing messages to be processed.
            mean_processing_time: The average time each message takes to be processed.
            failure_rate: The probability that sending a message will fail.
        """
        super().__init__()
        self.message_queue = message_queue
        self.mean_processing_time = mean_processing_time
        self.failure_rate = failure_rate
        self.sent_count: int = 0
        self.failed_count: int = 0

    def run(self) -> None:
        """
        Processes messages from the message queue until it is empty.
        For each message, waits for a random period of time based
        then attempts to send the message

        Returns:
            None
        """
        while not self.message_queue.empty():
            phone_number, message = self.message_queue.get()
            time.sleep(self._get_random_sleep_time())
            self._simulate_send(phone_number, message)
            self.message_queue.task_done()

    def _get_random_sleep_time(self) -> float:
        """
        Calculates a random sleep time using random.gauss centered around
        the mean processing time, with a minimum of 0.1 seconds.

        Returns:
            float: The sleep time in seconds before attempting to send the next message.
        """
        return max(0.1, random.gauss(self.mean_processing_time, 0.5))

    def _simulate_send(self, phone_number: str, message: str) -> None:
        """
        Simulates sending a message to a given phone number. This method randomly determines
        if the send operation succeeds or fails based on the configured failure rate.

        Parameters:
            phone_number (str): The recipient's phone number.
            message (str): The message content.

        Returns:
            None
        """
        if random.random() < self.failure_rate:
            self.failed_count += 1
        else:
            self.sent_count += 1
