"""Utility functions and objects."""


from enum import Enum


class JobStatus(Enum):
    """Represent the status of a job

        - UNKNOWN: Given that a runner can run on a different network,
            a job has an unknown status if the connection between the Scheduler
            and the Runner can't be established'.
        - SLEEPING: Waiting for a scheduled epoch to run
        - WAITING: Ready to run and waiting for a runner
        - RUNNING: Currently running
        - TERMINATED: Terminated by itself or by a runner after an error
        - DONE: Successfully executed
    """
    UNKNOWN = 0
    SLEEPING = 1
    WAITING = 2
    RUNNING = 3
    TERMINATED = 4
    DONE = 5


def is_status_valid(status):
    """Checks if the status value is valid"""
    if isinstance(status, str):
        res = status in ["UNKNOWN", "SLEEPING", "WAITING", "RUNNING", "TERMINATED", "DONE"]
    elif isinstance(status, int):
        res = 0 <= status <= 5
    else:
        return False
    return res
