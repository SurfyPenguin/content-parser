from argparse import ArgumentParser
from collections.abc import Callable

type Operation = Callable[[str], str]

class CLI:
    def __init__(self, parser: ArgumentParser) -> None:
        self.parser: ArgumentParser = parser
        self.registry = {}

    def init(self, func: Callable[[ArgumentParser], None]) -> None:
        func(self.parser)
        return func
    
    def register(self, label: str) -> Callable[[Operation], Operation]:
        def decorator(func: Operation) -> Operation:
            self.registry[label] = func
            return func
        return decorator
    
    def pipeline(self, *ops: str) -> Callable[[str], str]:
        def operator(content: str) -> str:
            for op in ops:
                func = self.registry.get(op)
                if func is None:
                    raise KeyError(f"{op}: function not registered")
                content = func(content)
            return content
        return operator
