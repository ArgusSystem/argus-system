from ..src.application import run
from time import sleep


with run('counting_application') as application:
    for i in range(10):
        print(i)
        sleep(1)
