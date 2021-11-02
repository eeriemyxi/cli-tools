import argparse
import os
from simpleeval import simple_eval
from typing import Callable


class FunctionInfo:
    def __init__(self, name: str, instance: Callable, kwargs: dict) -> None:
        self.name = name
        self.instance = instance
        self.kwargs = kwargs


class Argparse:
    def __init__(self, **kwargs) -> None:
        self.functions = list()
        self.parser = argparse.ArgumentParser(**kwargs)

    def add_command(self, **kwargs) -> Callable:
        def inner(func):
            self.functions.append(FunctionInfo(func.__name__, func, kwargs))

        return inner

    def start(self) -> None:
        for function in self.functions:
            dest = function.kwargs.get("dest") or function.name
            self.parser.add_argument(dest, **function.kwargs)
        args = self.parser.parse_args()
        for function in self.functions:
            dest = function.kwargs.get("dest") or function.name
            attr = getattr(args, dest)
            if attr:
                function.instance(attr)


argparse = Argparse(description="Basic but useful CLI tools.")


@argparse.add_command(
    metavar="<filename>", help="Create a new empty file.", dest="--mkfile"
)
def mkfile_command(string):
    current_directory = os.getcwd()
    file_directory = os.path.join(current_directory, string)
    if os.path.exists(file_directory):
        print("Path already exists.")
    else:
        open(file_directory, "w").close()
        print("File has been created.")


@argparse.add_command(
    metavar="<expression>",
    help="Safely evaluate an expression. Could be used as a basic calculator too.",
    dest="--eval",
)
def eval_command(string):
    execution = simple_eval(string)
    print(execution)


argparse.start()
