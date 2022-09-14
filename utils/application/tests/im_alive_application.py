from ..src.application import run
from time import sleep


with run('endless_application') as application:
    time_alive = 0

    while not application.is_stopped():
        print(f"I've been alive for {time_alive} seconds!")
        sleep(1)
        time_alive += 1

