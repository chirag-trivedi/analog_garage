import threading
import logging
from src.messageproducer import MessageProducer
from src.messagesender import MessageSender
from src.progressmonitor import ProgressMonitor
from src.userinput import get_user_input
from typing import Dict, Union
from utils.log_formatter import JsonFormatter


def configure_logging() -> None:
    """
    Configures the logging settings for the application.

    Returns:
        None
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(JsonFormatter())
    logger.addHandler(stream_handler)


def main(user_input: Dict[str, Union[int, float]]) -> None:
    """
    Configures logging, initializes and starts the producer, sender threads, and progress monitor.

    Parameters:
        user_input  Configuration values including the number of messages,
                                                   number of senders, mean processing time, failure rate,
                                                   and update interval.

    Returns:
        None
    """
    configure_logging()
    logging.getLogger("Main")

    num_messages = user_input["num_messages"]
    num_senders = user_input["num_senders"]
    mean_processing_time = user_input["mean_processing_time"]
    failure_rate = user_input["failure_rate"]
    update_interval = user_input["update_interval"]

    # Create producer and queue
    producer = MessageProducer(num_messages)
    message_queue = producer.messages

    # Start producer thread
    producer_thread = threading.Thread(target=producer.produce_messages, daemon=True)
    producer_thread.start()

    # Create and start sender threads
    senders = create_senders(
        message_queue, num_senders, mean_processing_time, failure_rate
    )

    # Start progress monitor
    monitor = ProgressMonitor(senders, update_interval)
    monitor.start()

    # Wait for all threads to finish
    producer_thread.join()
    for sender in senders:
        sender.join()
    monitor.join()


def create_senders(
    queue, num_senders: int, mean_processing_time: float, failure_rate: float
):
    """
    Creates and starts a specified number of message sender threads, each configured with
    a given mean processing time and failure rate. The sender threads will pull messages
    from the shared queue and simulate sending them.

    Parameters:
        queue : The shared message queue from which each sender will pull messages.
        num_senders  The number of sender threads to create.
        mean_processing_time The average processing time for sending each message.
        failure_rate : The probability of message sending failure.

    Returns:
        A list of active MessageSender threads.
    """
    senders = [
        MessageSender(queue, mean_processing_time, failure_rate)
        for _ in range(num_senders)
    ]
    for sender in senders:
        sender.start()
    return senders


if __name__ == "__main__":
    user_input = get_user_input()

    try:
        main(user_input)
    except KeyboardInterrupt:
        logging.getLogger("Main").info("Process interrupted by user.")
    except Exception as e:
        logging.getLogger("Main").error(f"Unexpected error occurred: {e}")
