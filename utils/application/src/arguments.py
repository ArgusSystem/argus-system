from argparse import ArgumentParser, ArgumentTypeError
import os.path as path
import re


def _yaml_type(arg_value):
    pattern = re.compile(r'.+\.yml')

    if not pattern.match(arg_value):
        raise ArgumentTypeError('Value must be a YAML file!')

    if not path.exists(arg_value):
        raise ArgumentTypeError('File not found!')

    return arg_value


def parse_arguments(application_name):
    parser = ArgumentParser(description=application_name)
    parser.add_argument('--config_file', '-c',
                        type=_yaml_type,
                        required=True,
                        help="Configuration file to set up the application")

    return parser.parse_args()
