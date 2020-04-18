import os

__all__ = [
    'TextStyle',
    'make_directory_tree'
]


class TextStyle(object):
    _BOLD = '\033[1m'
    _PURPLE = '\033[95m'
    _CYAN = '\033[96m'
    _DARKCYAN = '\033[36m'
    _BLUE = '\033[94m'
    _GREEN = '\033[92m'
    _YELLOW = '\033[93m'
    _RED = '\033[91m'
    _UNDERLINE = '\033[4m'
    _END = '\033[0m'

    @staticmethod
    def bold(string):
        return TextStyle._BOLD + string + TextStyle._END

    @staticmethod
    def red(string):
        return TextStyle._RED + string + TextStyle._END


def make_directory_tree(manbrew_root):
    os.makedirs(os.path.join(manbrew_root, 'Containers'), exist_ok=True)
