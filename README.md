# SMS Simulation Exercise

This project simulates sending a large number of SMS alerts, designed for applications like emergency alert services. The simulation consists of three main parts

1. **Message Producer**: Generates a configurable number of messages (default: 1000) directed to random phone numbers. Each message can contain up to 100 random characters.
2. **Message Senders**: A configurable number of sender threads that pick up messages from the producer. Each sender simulates sending messages by waiting a random period distributed around a configurable mean processing time. The senders also have a configurable failure rate to simulate message delivery failures.
3. **Progress Monitor**: Tracks and displays real-time statistics, updating every N seconds (configurable). The monitor shows:
   - The number of messages sent so far
   - The number of messages failed
   - The average time taken per message

## Requirements

- Python 3.10+
- Libraries: `python-dotenv`

## Usage

To run the simulation with default settings:

python main.py

To override default settings using command-line arguments

-m --num_messages
-s --num_senders
-t --mean_processing_time
-f --failure_rate
-u --update_interval

python main.py -m 20 -s 10 -t 0.7 -f 0.05 -u 3


## Testing

python -m unittest tests/test.py


## Next Steps

1) split producer,sender and progress monitor invocation
2) add docker , docker compose
3) cythonize the code
4) use of rabbitmq or aws sqs
5) add more functional tests using cypress
6) add a UI to configure options from the FE and show progress monitor
7) Use of grafana or splunk to track message success and failure over time ie via dashboards