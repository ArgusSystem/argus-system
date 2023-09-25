from .classification_notifier import ClassificationNotifier
from .web_notifier import WebNotifier

TYPE = 'type'

NOTIFIERS = {
    'classification': ClassificationNotifier,
    'web': WebNotifier
}


def create_notifier(configuration):
    notifier_type = configuration[TYPE]

    if notifier_type in NOTIFIERS:
        notifier_configuration = configuration[notifier_type]
        return NOTIFIERS[notifier_type](notifier_configuration)

    raise RuntimeError(f'Invalid notifier {notifier_type}')
