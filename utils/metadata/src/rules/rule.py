from .when import WhenRule
from .where import Where, WhereRule
from .who import Who, WhoRule

WHO = 'who'
WHERE = 'where'
WHEN = 'when'


class Rule:

    def __init__(self, _id, configuration, last_update):
        self.id = _id
        self.who_rule = WhoRule(configuration[WHO])
        self.where_rule = WhereRule(configuration[WHERE])
        self.when_rule = WhenRule(configuration[WHEN])
        self.last_update = last_update

    def match(self, person, role, camera, area, area_type, timestamp):
        return self.who_rule.match(Who(person, role)) and \
            self.where_rule.match(Where(camera, area, area_type)) and \
            self.when_rule.match(timestamp)

