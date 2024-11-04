import threading
import logging
import time
from typing import List


class ProgressMonitor(threading.Thread):
    def __init__(self, senders: List, update_interval: int) -> None:
        """
        Initializes the ProgressMonitor with a list of sender threads and an update interval.

        Parameters:
            senders: A list of MessageSender instances that are sending messages.
            update_interval: The time interval at which progress updates are logged.
        """
        super().__init__()

        self.logger = logging.getLogger("Monitor")

        self.senders = senders
        self.update_interval = update_interval
        self.total_sent = 0
        self.total_failed = 0
        self.start_time = time.time()

    def run(self) -> None:
        """
        Starts monitoring the progress of the sender threads.
        While any sender is still active, it waits for the specified update interval and then logs progress updates.

        Returns:
            None
        """
        while any(sender.is_alive() for sender in self.senders):
            time.sleep(self.update_interval)
            self.update_progress()

    def update_progress(self) -> None:
        """
        This method calculates and logs the current progress of the message-sending operation.

        Returns:
            None
        """
        self.total_sent: int = sum(sender.sent_count for sender in self.senders)
        self.total_failed: int = sum(sender.failed_count for sender in self.senders)
        total_messages: int = self.total_sent + self.total_failed
        elapsed_time = time.time() - self.start_time
        avg_time_per_message: float = (
            elapsed_time / total_messages if total_messages > 0 else 0
        )

        self.logger.info(
            f"Messages Sent: {self.total_sent}, Messages Failed: {self.total_failed}, Average Time per Message: {avg_time_per_message:.2f} seconds"
        )
