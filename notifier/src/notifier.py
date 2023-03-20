class Notifier:

    def __init__(self, tracer):
        self.tracer = tracer

    def on_broken_rule(self, broken_rule):
        print('New Message')
