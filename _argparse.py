import argparse
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

    def instigate(self) -> None:
        for function in self.functions:
            dest = function.kwargs.get("dest") or function.name
            self.parser.add_argument(dest, **function.kwargs)
        args = self.parser.parse_args()
        for function in self.functions:
            dest = function.kwargs.get("dest") or function.name
            attr = getattr(args, dest)
            if attr:
                function.instance(attr)