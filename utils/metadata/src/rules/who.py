from .factory import create


class Person:

    def __init__(self, people):
        self.people = people

    def match(self, who):
        return who.person in self.people


class Role:

    def __init__(self, roles):
        self.roles = roles

    def match(self, who):
        return who.role in self.roles


class Unknown:

    def __init__(self, _):
        pass

    def match(self, who):
        return who.person is None


class All:

    def __init__(self, _):
        pass

    def match(self, _):
        return True


TYPES = {
    'person': Person,
    'role': Role,
    'unknown': Unknown,
    'all': All
}


class Who:

    def __init__(self, person, role):
        self.person = person
        self.role = role


class WhoRule:

    def __init__(self, configuration):
        self.rules = [create(TYPES, node) for node in configuration]

    def match(self, who):
        return any(rule.match(who) for rule in self.rules)
