import argparse
from core import sub_commands

__all__ = ["ArgParser"]


_ALL_ARGS = [
    # subcommand link
    {"name": "link",
     "help": "link container.",
     "args": [{"str": "container",
               "kwargs": {"type": str,
                          "help": "the container to link."}},
              {"str": "--dst",
               "kwargs": {"type": str,
                          "default": "/usr/local",
                          "help": "path where symbol links go, just use '/usr/local'."}}]},

    # subcommand unlink
    {"name": "unlink",
     "help": "unlink container.",
     "args": [{"str": "container",
               "kwargs": {"type": str,
                          "help": "the container to unlink."}}]},

    # subcommand remove
    {"name": "remove",
     "help": "remove container.",
     "args": [{"str": "container",
               "kwargs": {"type": str,
                          "help": "the container to remove."}}]},

    # subcommand list
    {"name": "list",
     "help": "list all containers.",
     "args": []},

    # subcommand root
    {"name": "root",
     "help": "print manbrew root.",
     "args": []}
]


class ArgParser(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser(description="Manage manually installed libraries.")
        subparsers = self._parser.add_subparsers(
            title="subcommands", description="valid subcommands",
            help="Use 'manbrew subcommand --help' to see more helps."
        )
        for sub_command in _ALL_ARGS:
            parser = subparsers.add_parser(sub_command['name'], help=sub_command['help'])
            parser.set_defaults(func=getattr(sub_commands, sub_command['name'] + '_command'))
            for arg in sub_command['args']:
                parser.add_argument(arg['str'], **arg['kwargs'])
            parser.add_argument("--log", type=str, default="INFO",
                                help="log level.")

    def parse(self):
        return self._parser.parse_args()
