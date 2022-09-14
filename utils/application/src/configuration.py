import yaml
from collections import defaultdict


def load_configuration(configuration_filepath):
    with open(configuration_filepath, 'r') as file:
        configuration = yaml.safe_load(file)

    return defaultdict(dict, configuration)
