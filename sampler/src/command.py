import os


class CommandError(Exception):

    def __init__(self, message):
        super().__init__(message)


def run(command):
    result = os.system(command)

    if result != 0:
        raise CommandError(f"Non-zero result({result}) after executing: '{command}'")
