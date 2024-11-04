import os
from dotenv import load_dotenv
import argparse
from dataclasses import dataclass, field
from typing import Dict, Union

# Load environment variables
load_dotenv()


@dataclass
class Config:
    """
    dataclass that loads default settings from environment variables,
    with options to override them via command-line arguments.

    """

    num_messages: int = field(
        default_factory=lambda: get_env_variable("NUMBER_OF_MESSAGES", int)
    )
    num_senders: int = field(
        default_factory=lambda: get_env_variable("NUMBER_OF_SENDERS", int)
    )
    mean_processing_time: float = field(
        default_factory=lambda: get_env_variable("MEAN_PROCESSING_TIME", float)
    )
    failure_rate: float = field(
        default_factory=lambda: get_env_variable("FAILURE_RATE", float)
    )
    update_interval: int = field(
        default_factory=lambda: get_env_variable("UPDATE_INTERVAL", int)
    )

    @classmethod
    def from_args(cls) -> "Config":
        """
        THis creates a Config instance by parsing command-line arguments or the
        environment variables.

        Returns:
            A configuration instance.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("-m", "--num_messages", type=int, help="Number of messages")
        parser.add_argument("-s", "--num_senders", type=int, help="Number of senders")
        parser.add_argument(
            "-t", "--mean_processing_time", type=float, help="Mean processing time"
        )
        parser.add_argument("-f", "--failure_rate", type=float, help="Failure rate")
        parser.add_argument("-u", "--update_interval", type=int, help="Update interval")
        args = parser.parse_args()

        # Create a Config instance, overriding env defaults with any command-line arguments provided
        return cls(
            num_messages=args.num_messages or cls().num_messages,
            num_senders=args.num_senders or cls().num_senders,
            mean_processing_time=args.mean_processing_time
            or cls().mean_processing_time,
            failure_rate=args.failure_rate or cls().failure_rate,
            update_interval=args.update_interval or cls().update_interval,
        )


def get_env_variable(name: str, cast_type: type) -> Union[int, float]:
    """
    Retrieves an environment variable.

    Parameters:
        name: The name of the environment variable.
        cast_type The type to cast the environment variable .

    Returns:
        The value of the environment variable, cast to the specified type.

    Raises:
        A ValueError if the environment variable is not set.
    """
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Environment variable '{name}' not set.")
    return cast_type(value)


def get_user_input() -> Dict[str, Union[int, float]]:
    """
    gets and returns the configuration settings from command-line arguments or environment variables.

    """
    config = Config.from_args()
    return {
        "num_messages": config.num_messages,
        "num_senders": config.num_senders,
        "mean_processing_time": config.mean_processing_time,
        "failure_rate": config.failure_rate,
        "update_interval": config.update_interval,
    }
