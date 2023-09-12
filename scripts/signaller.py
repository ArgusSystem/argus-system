import os
import signal


def signal_sigint(pid=os.getpid()):
    os.kill(pid, signal.SIGINT)
