from .when import WhenRule
from .where import Where, WhereRule
from .who import Who, WhoRule

WHO = 'who'
WHERE = 'where'
WHEN = 'when'


class Rule:

    def __init__(self, _id, configuration):
        self._id = _id
        self.who_rule = WhoRule(configuration[WHO])
        self.where_rule = WhereRule(configuration[WHERE])
        self.when_rule = WhenRule(configuration[WHEN])

    def match(self, person, camera, timestamp):
        return self.who_rule.match(Who(person.id, person.role.id)) and \
            self.where_rule.match(Where(camera.id, camera.area.id, camera.area.area_type.id)) and \
            self.when_rule.match(timestamp)

