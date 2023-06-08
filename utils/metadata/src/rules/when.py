from datetime import date

from .factory import create

START_TIME = 'start_time'
END_TIME = 'end_time'
DAYS = 'days'


class Single:

    def __init__(self, configuration):
        self.start_time = configuration[START_TIME]
        self.end_time = configuration[END_TIME]

    def match(self, timestamp):
        return self.start_time <= timestamp <= self.end_time


class Repeated:

    def __init__(self, configuration):
        self.start_time = configuration[START_TIME]
        self.end_time = configuration[END_TIME]
        self.days = configuration[DAYS]

    def match(self, timestamp):
        datetime = date.fromtimestamp(timestamp)
        time_tuple = datetime.timetuple()
        time = time_tuple.tm_hour * 3600 + time_tuple.tm_min * 60 + time_tuple.tm_sec

        return datetime.strftime('%A') in self.days and self.start_time <= time <= self.end_time


TYPES = {
    'single': Single,
    'repeated': Repeated
}


class WhenRule:

    def __init__(self, configuration):
        self.rules = [create(TYPES, node) for node in configuration]

    def match(self, when):
        return any(rule.match(when) for rule in self.rules)
