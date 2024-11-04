import unittest
import queue
from unittest.mock import MagicMock, patch
import logging
import time

from src.messageproducer import MessageProducer
from src.messagesender import MessageSender
from src.progressmonitor import ProgressMonitor


class TestMessageProducer(unittest.TestCase):
    def test_random_phone_number(self):
        phone_number = MessageProducer.get_random_phone_number()
        self.assertRegex(phone_number, r"^\+1\d{10}$")

    def test_random_message_length(self):
        message = MessageProducer.get_random_message()
        self.assertGreater(len(message), 0)
        self.assertLess(len(message), 101)

    def test_message_generation(self):
        producer = MessageProducer(num_messages=10)
        producer.produce_messages()
        self.assertEqual(producer.messages.qsize(), 10)


class TestMessageSender(unittest.TestCase):
    def test_sender_processing(self):
        message_queue = queue.Queue()
        message_queue.put(("+9876543210", "A Test message"))

        sender = MessageSender(
            message_queue, mean_processing_time=0.1, failure_rate=0.0
        )
        sender.start()
        sender.join()

        self.assertEqual(sender.sent_count, 1)
        self.assertEqual(sender.failed_count, 0)


class TestProgressMonitor(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger("Monitor")
        self.logger.setLevel(logging.INFO)
        self.log_stream = MagicMock()
        handler = logging.StreamHandler(self.log_stream)
        self.logger.addHandler(handler)

    def test_initialization(self):
        sender_mock = MagicMock()
        monitor = ProgressMonitor(senders=[sender_mock], update_interval=1)

        self.assertEqual(monitor.update_interval, 1)
        self.assertEqual(len(monitor.senders), 1)
        self.assertEqual(monitor.total_sent, 0)
        self.assertEqual(monitor.total_failed, 0)

    @patch("time.sleep", return_value=None)
    def test_progress_update(self, mock_sleep):
        sender1 = MagicMock()
        sender2 = MagicMock()
        sender1.sent_count = 5
        sender1.failed_count = 2
        sender2.sent_count = 3
        sender2.failed_count = 1

        monitor = ProgressMonitor(senders=[sender1, sender2], update_interval=1)
        monitor.start_time = time.time() - 10

        monitor.update_progress()

        self.assertEqual(monitor.total_sent, 8)
        self.assertEqual(monitor.total_failed, 3)

        self.logger.info = MagicMock()
        monitor.update_progress()
        self.logger.info.assert_called_once()

        logged_message = self.logger.info.call_args[0][0]
        self.assertIn("Messages Sent: 8", logged_message)
        self.assertIn("Messages Failed: 3", logged_message)


if __name__ == "__main__":
    unittest.main()
